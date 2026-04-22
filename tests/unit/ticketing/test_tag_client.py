import pytest

from libzapi.domain.errors import NotFound, Unauthorized
from libzapi.infrastructure.api_clients.ticketing import TagApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.tag_api_client.yield_items"
    )


# ---------------------------------------------------------------------------
# list_account
# ---------------------------------------------------------------------------


def test_list_account_delegates_to_yield_items(http, yield_items):
    yield_items.return_value = iter([{"name": "a", "count": 1}])
    client = TagApiClient(http)
    out = list(client.list_account())
    yield_items.assert_called_once_with(
        get_json=http.get,
        first_path="/api/v2/tags",
        base_url=http.base_url,
        items_key="tags",
    )
    assert out == [{"name": "a", "count": 1}]


# ---------------------------------------------------------------------------
# list_for
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "resource, path",
    [
        ("ticket", "/api/v2/tickets/42/tags"),
        ("user", "/api/v2/users/42/tags"),
        ("organization", "/api/v2/organizations/42/tags"),
    ],
)
def test_list_for_resource_hits_expected_path(http, resource, path):
    http.get.return_value = {"tags": ["foo", "bar"]}
    client = TagApiClient(http)
    result = client.list_for(resource=resource, resource_id=42)
    http.get.assert_called_with(path)
    assert result == ["foo", "bar"]


def test_list_for_missing_tags_returns_empty_list(http):
    http.get.return_value = {}
    client = TagApiClient(http)
    assert client.list_for(resource="ticket", resource_id=1) == []


def test_invalid_resource_raises_value_error(http):
    client = TagApiClient(http)
    with pytest.raises(ValueError, match="resource must be one of"):
        client.list_for(resource="group", resource_id=1)


# ---------------------------------------------------------------------------
# add / set / remove
# ---------------------------------------------------------------------------


def test_add_puts_tags_and_returns_list(http):
    http.put.return_value = {"tags": ["foo", "bar", "baz"]}
    client = TagApiClient(http)
    result = client.add(resource="ticket", resource_id=42, tags=iter(["baz"]))
    http.put.assert_called_with(
        "/api/v2/tickets/42/tags", {"tags": ["baz"]}
    )
    assert result == ["foo", "bar", "baz"]


def test_set_posts_tags_and_returns_list(http):
    http.post.return_value = {"tags": ["only", "these"]}
    client = TagApiClient(http)
    result = client.set(resource="user", resource_id=7, tags=["only", "these"])
    http.post.assert_called_with(
        "/api/v2/users/7/tags", {"tags": ["only", "these"]}
    )
    assert result == ["only", "these"]


def test_remove_deletes_with_json_body(http):
    http.delete.return_value = {"tags": ["remaining"]}
    client = TagApiClient(http)
    result = client.remove(
        resource="organization", resource_id=9, tags=["gone"]
    )
    http.delete.assert_called_with(
        "/api/v2/organizations/9/tags",
        json={"tags": ["gone"]},
    )
    assert result == ["remaining"]


def test_remove_handles_none_response(http):
    http.delete.return_value = None
    client = TagApiClient(http)
    assert client.remove(resource="ticket", resource_id=1, tags=["x"]) == []


def test_add_missing_tags_key_returns_empty(http):
    http.put.return_value = {}
    client = TagApiClient(http)
    assert client.add(resource="ticket", resource_id=1, tags=["x"]) == []


def test_set_missing_tags_key_returns_empty(http):
    http.post.return_value = {}
    client = TagApiClient(http)
    assert client.set(resource="ticket", resource_id=1, tags=["x"]) == []


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_list_for_propagates_error(error_cls, http):
    http.get.side_effect = error_cls("boom")
    client = TagApiClient(http)
    with pytest.raises(error_cls):
        client.list_for(resource="ticket", resource_id=1)
