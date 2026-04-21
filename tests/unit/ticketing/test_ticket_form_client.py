import pytest

from libzapi.application.commands.ticketing.ticket_form_cmds import (
    CreateTicketFormCmd,
    UpdateTicketFormCmd,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)
from libzapi.infrastructure.api_clients.ticketing import TicketFormApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_form_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# Listing / pagination
# ---------------------------------------------------------------------------


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "ticket_forms": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketFormApiClient(http)
    result = list(client.list())
    http.get.assert_called_with("/api/v2/ticket_forms")
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_get_returns_domain(http, domain):
    http.get.return_value = {"ticket_form": {"id": 5}}
    client = TicketFormApiClient(http)
    result = client.get(ticket_form_id=5)
    http.get.assert_called_with("/api/v2/ticket_forms/5")
    assert result["id"] == 5


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"ticket_form": {"id": 1, "name": "F"}}
    client = TicketFormApiClient(http)
    result = client.create(
        CreateTicketFormCmd(name="F", ticket_field_ids=[1, 2])
    )
    http.post.assert_called_with(
        "/api/v2/ticket_forms",
        {"ticket_form": {"name": "F", "ticket_field_ids": [1, 2]}},
    )
    assert result["name"] == "F"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"ticket_form": {"id": 1, "active": False}}
    client = TicketFormApiClient(http)
    client.update(ticket_form_id=1, entity=UpdateTicketFormCmd(active=False))
    http.put.assert_called_with(
        "/api/v2/ticket_forms/1", {"ticket_form": {"active": False}}
    )


def test_delete_calls_delete(http):
    client = TicketFormApiClient(http)
    client.delete(ticket_form_id=7)
    http.delete.assert_called_with("/api/v2/ticket_forms/7")


# ---------------------------------------------------------------------------
# clone / reorder
# ---------------------------------------------------------------------------


def test_clone_posts_empty_body(http, domain):
    http.post.return_value = {"ticket_form": {"id": 9}}
    client = TicketFormApiClient(http)
    result = client.clone(ticket_form_id=5)
    http.post.assert_called_with("/api/v2/ticket_forms/5/clone", {})
    assert result["id"] == 9


def test_reorder_puts_ids(http):
    client = TicketFormApiClient(http)
    client.reorder(ticket_form_ids=[3, 1, 2])
    http.put.assert_called_with(
        "/api/v2/ticket_forms/reorder", {"ticket_form_ids": [3, 1, 2]}
    )


def test_reorder_converts_iterable(http):
    client = TicketFormApiClient(http)
    client.reorder(ticket_form_ids=iter([3, 1]))
    http.put.assert_called_with(
        "/api/v2/ticket_forms/reorder", {"ticket_form_ids": [3, 1]}
    )


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
def test_ticket_form_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = TicketFormApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
