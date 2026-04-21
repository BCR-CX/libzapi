import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.application.commands.ticketing.view_cmds import (
    CreateViewCmd,
    UpdateViewCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.ticketing.view import View
from libzapi.infrastructure.api_clients.ticketing import ViewApiClient


view_strategy = builds(
    View,
    raw_title=just("Base View"),
)


@given(view_strategy)
def test_view_logical_key_from_raw_title(view):
    assert view.logical_key.as_str() == "view:base_view"


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.view_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# Listing / pagination endpoints
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method_name, expected_path",
    [
        ("list_all", "/api/v2/views"),
        ("list_active", "/api/v2/views/active"),
    ],
)
def test_list_endpoints(method_name, expected_path, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"views": []}
    client = ViewApiClient(https)
    list(getattr(client, method_name)())
    https.get.assert_called_with(expected_path)


def test_list_all_yields_items(http, domain):
    http.get.return_value = {
        "views": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = ViewApiClient(http)
    assert len(list(client.list_all())) == 2


def test_list_active_yields_items(http, domain):
    http.get.return_value = {
        "views": [{"id": 1}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = ViewApiClient(http)
    assert len(list(client.list_active())) == 1


def test_search_yields_items(http, domain):
    http.get.return_value = {
        "views": [{"id": 7}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = ViewApiClient(http)
    result = list(client.search(query="libzapi"))
    http.get.assert_called_with("/api/v2/views/search?query=libzapi")
    assert len(result) == 1


# ---------------------------------------------------------------------------
# Count / execute
# ---------------------------------------------------------------------------


def test_count_returns_snapshot(http):
    http.get.return_value = {
        "count": {"refreshed_at": "2024-01-01T00:00:00Z", "value": 42}
    }
    client = ViewApiClient(http)
    result = client.count()
    http.get.assert_called_with("/api/v2/views/count")
    assert result.value == 42


def test_count_view_returns_view_count(http):
    http.get.return_value = {
        "view_count": {"view_id": 5, "value": 10}
    }
    client = ViewApiClient(http)
    result = client.count_view(view_id=5)
    http.get.assert_called_with("/api/v2/views/5/count")
    assert result == {"view_id": 5, "value": 10}


def test_count_view_handles_missing_key(http):
    http.get.return_value = {}
    client = ViewApiClient(http)
    assert client.count_view(view_id=5) == {}


def test_count_many_returns_list(http):
    http.get.return_value = {
        "view_counts": [
            {"view_id": 1, "value": 3},
            {"view_id": 2, "value": 4},
        ]
    }
    client = ViewApiClient(http)
    result = client.count_many([1, 2])
    http.get.assert_called_with("/api/v2/views/count_many?ids=1,2")
    assert len(result) == 2


def test_count_many_handles_missing_key(http):
    http.get.return_value = {}
    client = ViewApiClient(http)
    assert client.count_many([1]) == []


def test_execute_returns_dict(http):
    http.get.return_value = {"rows": [], "columns": []}
    client = ViewApiClient(http)
    assert client.execute(view_id=5) == {"rows": [], "columns": []}
    http.get.assert_called_with("/api/v2/views/5/execute")


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


def test_get_returns_domain(http, domain):
    http.get.return_value = {"view": {"id": 5}}
    client = ViewApiClient(http)
    result = client.get(view_id=5)
    http.get.assert_called_with("/api/v2/views/5")
    assert result["id"] == 5


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"view": {"id": 1, "title": "V"}}
    client = ViewApiClient(http)
    client.create(CreateViewCmd(title="V"))
    http.post.assert_called_with("/api/v2/views", {"view": {"title": "V"}})


def test_update_puts_payload(http, domain):
    http.put.return_value = {"view": {"id": 1, "active": False}}
    client = ViewApiClient(http)
    client.update(view_id=1, entity=UpdateViewCmd(active=False))
    http.put.assert_called_with(
        "/api/v2/views/1", {"view": {"active": False}}
    )


def test_delete_calls_delete(http):
    client = ViewApiClient(http)
    client.delete(view_id=7)
    http.delete.assert_called_with("/api/v2/views/7")


# ---------------------------------------------------------------------------
# Bulk operations
# ---------------------------------------------------------------------------


def test_update_many_puts_bodies_with_ids(http, domain):
    http.put.return_value = {"job_status": {"id": "abc"}}
    client = ViewApiClient(http)
    client.update_many(
        [
            (1, UpdateViewCmd(active=False)),
            (2, UpdateViewCmd(description="n")),
        ]
    )
    http.put.assert_called_with(
        "/api/v2/views/update_many",
        {
            "views": [
                {"active": False, "id": 1},
                {"description": "n", "id": 2},
            ]
        },
    )


def test_destroy_many_deletes_with_ids(http, domain):
    http.delete.return_value = {"job_status": {"id": "abc"}}
    client = ViewApiClient(http)
    client.destroy_many([1, 2])
    http.delete.assert_called_with("/api/v2/views/destroy_many?ids=1,2")


def test_destroy_many_handles_none_response(http, domain):
    http.delete.return_value = None
    client = ViewApiClient(http)
    with pytest.raises(KeyError):
        client.destroy_many([1])


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = ViewApiClient(https)
    with pytest.raises(error_cls):
        list(client.list_all())
