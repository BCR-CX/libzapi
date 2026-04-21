import pytest

from libzapi.application.commands.ticketing.ticket_field_cmds import (
    CreateTicketFieldCmd,
    TicketFieldOptionCmd,
    UpdateTicketFieldCmd,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)
from libzapi.infrastructure.api_clients.ticketing import TicketFieldApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_field_api_client.to_domain",
        side_effect=lambda data, cls: {**(data or {})},
    )


# ---------------------------------------------------------------------------
# Listing / pagination
# ---------------------------------------------------------------------------


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "ticket_fields": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketFieldApiClient(http)
    result = list(client.list())
    http.get.assert_called_with("/api/v2/ticket_fields")
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_get_returns_domain(http, domain):
    http.get.return_value = {"ticket_field": {"id": 5}}
    client = TicketFieldApiClient(http)
    result = client.get(field_id=5)
    http.get.assert_called_with("/api/v2/ticket_fields/5")
    assert result["id"] == 5


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"ticket_field": {"id": 1, "title": "Order"}}
    client = TicketFieldApiClient(http)
    result = client.create(
        CreateTicketFieldCmd(title="Order", type="text", required=True)
    )
    http.post.assert_called_with(
        "/api/v2/ticket_fields",
        {"ticket_field": {"title": "Order", "type": "text", "required": True}},
    )
    assert result["title"] == "Order"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"ticket_field": {"id": 1, "active": False}}
    client = TicketFieldApiClient(http)
    client.update(field_id=1, entity=UpdateTicketFieldCmd(active=False))
    http.put.assert_called_with(
        "/api/v2/ticket_fields/1", {"ticket_field": {"active": False}}
    )


def test_delete_calls_delete(http):
    client = TicketFieldApiClient(http)
    client.delete(field_id=7)
    http.delete.assert_called_with("/api/v2/ticket_fields/7")


# ---------------------------------------------------------------------------
# reorder
# ---------------------------------------------------------------------------


def test_reorder_puts_ids(http):
    client = TicketFieldApiClient(http)
    client.reorder(field_ids=[3, 1, 2])
    http.put.assert_called_with(
        "/api/v2/ticket_fields/reorder", {"ticket_field_ids": [3, 1, 2]}
    )


def test_reorder_converts_iterable(http):
    client = TicketFieldApiClient(http)
    client.reorder(field_ids=iter([3, 1]))
    http.put.assert_called_with(
        "/api/v2/ticket_fields/reorder", {"ticket_field_ids": [3, 1]}
    )


# ---------------------------------------------------------------------------
# options
# ---------------------------------------------------------------------------


def test_list_options_yields_items(http):
    http.get.return_value = {
        "custom_field_options": [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketFieldApiClient(http)
    result = list(client.list_options(field_id=5))
    http.get.assert_called_with("/api/v2/ticket_fields/5/options")
    assert len(result) == 2
    assert result[0]["name"] == "A"


def test_get_option_returns_item(http):
    http.get.return_value = {"custom_field_option": {"id": 7, "name": "A"}}
    client = TicketFieldApiClient(http)
    result = client.get_option(field_id=5, option_id=7)
    http.get.assert_called_with("/api/v2/ticket_fields/5/options/7")
    assert result == {"id": 7, "name": "A"}


def test_upsert_option_posts_payload(http):
    http.post.return_value = {"custom_field_option": {"id": 9, "name": "A"}}
    client = TicketFieldApiClient(http)
    result = client.upsert_option(
        field_id=5, option=TicketFieldOptionCmd(name="A", value="a")
    )
    http.post.assert_called_with(
        "/api/v2/ticket_fields/5/options",
        {"custom_field_option": {"name": "A", "value": "a"}},
    )
    assert result["id"] == 9


def test_upsert_option_with_id_posts_payload(http):
    http.post.return_value = {"custom_field_option": {"id": 9, "name": "A"}}
    client = TicketFieldApiClient(http)
    client.upsert_option(
        field_id=5, option=TicketFieldOptionCmd(name="A", value="a", id=9)
    )
    http.post.assert_called_with(
        "/api/v2/ticket_fields/5/options",
        {"custom_field_option": {"name": "A", "value": "a", "id": 9}},
    )


def test_delete_option_calls_delete(http):
    client = TicketFieldApiClient(http)
    client.delete_option(field_id=5, option_id=7)
    http.delete.assert_called_with("/api/v2/ticket_fields/5/options/7")


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
def test_ticket_field_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = TicketFieldApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
