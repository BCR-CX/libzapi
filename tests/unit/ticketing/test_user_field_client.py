import pytest

from libzapi.application.commands.ticketing.user_field_cmds import (
    CreateUserFieldCmd,
    UpdateUserFieldCmd,
    UserFieldOptionCmd,
)
from libzapi.infrastructure.api_clients.ticketing import UserFieldApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_field_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# Listing / pagination
# ---------------------------------------------------------------------------


def test_list_all_yields_items(http, domain):
    http.get.return_value = {
        "user_fields": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = UserFieldApiClient(http)
    result = list(client.list_all())
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_list_options_yields_items(http, domain):
    http.get.return_value = {
        "custom_field_options": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = UserFieldApiClient(http)
    result = list(client.list_options(user_field_id=5))
    http.get.assert_called_with("/api/v2/user_fields/5/options")
    assert len(result) == 2


# ---------------------------------------------------------------------------
# create / update / delete / reorder
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"user_field": {"id": 1, "key": "region"}}
    client = UserFieldApiClient(http)
    result = client.create(
        CreateUserFieldCmd(key="region", type="text", title="Region")
    )
    http.post.assert_called_with(
        "/api/v2/user_fields",
        {"user_field": {"key": "region", "type": "text", "title": "Region"}},
    )
    assert result["key"] == "region"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"user_field": {"id": 1, "active": False}}
    client = UserFieldApiClient(http)
    client.update(user_field_id=1, entity=UpdateUserFieldCmd(active=False))
    http.put.assert_called_with(
        "/api/v2/user_fields/1", {"user_field": {"active": False}}
    )


def test_delete_calls_delete(http):
    client = UserFieldApiClient(http)
    client.delete(user_field_id=7)
    http.delete.assert_called_with("/api/v2/user_fields/7")


def test_reorder_puts_ids(http):
    client = UserFieldApiClient(http)
    client.reorder(user_field_ids=[3, 1, 2])
    http.put.assert_called_with(
        "/api/v2/user_fields/reorder", {"user_field_ids": [3, 1, 2]}
    )


def test_reorder_converts_iterable(http):
    client = UserFieldApiClient(http)
    client.reorder(user_field_ids=iter([3, 1]))
    http.put.assert_called_with(
        "/api/v2/user_fields/reorder", {"user_field_ids": [3, 1]}
    )


# ---------------------------------------------------------------------------
# options
# ---------------------------------------------------------------------------


def test_upsert_option_posts_payload(http, domain):
    http.post.return_value = {"custom_field_option": {"id": 9, "name": "A"}}
    client = UserFieldApiClient(http)
    result = client.upsert_option(
        user_field_id=5, option=UserFieldOptionCmd(name="A", value="a")
    )
    http.post.assert_called_with(
        "/api/v2/user_fields/5/options",
        {"custom_field_option": {"name": "A", "value": "a"}},
    )
    assert result["id"] == 9


def test_upsert_option_with_id_posts_payload(http, domain):
    http.post.return_value = {"custom_field_option": {"id": 9}}
    client = UserFieldApiClient(http)
    client.upsert_option(
        user_field_id=5,
        option=UserFieldOptionCmd(name="A", value="a", id=9),
    )
    http.post.assert_called_with(
        "/api/v2/user_fields/5/options",
        {"custom_field_option": {"name": "A", "value": "a", "id": 9}},
    )


def test_delete_option_calls_delete(http):
    client = UserFieldApiClient(http)
    client.delete_option(user_field_id=5, user_field_option_id=7)
    http.delete.assert_called_with("/api/v2/user_fields/5/options/7")
