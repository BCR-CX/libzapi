import pytest

from libzapi.infrastructure.api_clients.ticketing.suspended_ticket_api_client import (
    SuspendedTicketApiClient,
)


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.suspended_ticket_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.suspended_ticket_api_client.yield_items"
    )


def test_list_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}, {"id": 2}])
    client = SuspendedTicketApiClient(http)
    result = list(client.list())
    assert [r["id"] for r in result] == [1, 2]
    assert all(r["_cls"] == "SuspendedTicket" for r in result)
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/suspended_tickets"
    assert kwargs["items_key"] == "suspended_tickets"


def test_get_reads_suspended_ticket_key(http, domain):
    http.get.return_value = {"suspended_ticket": {"id": 7}}
    client = SuspendedTicketApiClient(http)
    result = client.get(id_=7)
    http.get.assert_called_with("/api/v2/suspended_tickets/7")
    assert result["_cls"] == "SuspendedTicket"


def test_recover_puts_empty_body(http, domain):
    http.put.return_value = {"suspended_ticket": {"id": 7}}
    client = SuspendedTicketApiClient(http)
    result = client.recover(id_=7)
    http.put.assert_called_with("/api/v2/suspended_tickets/7/recover", {})
    assert result["_cls"] == "SuspendedTicket"


def test_recover_many_puts_ids_query(http):
    http.put.return_value = {"status": "ok"}
    client = SuspendedTicketApiClient(http)
    result = client.recover_many(ids=[1, 2, 3])
    http.put.assert_called_with(
        "/api/v2/suspended_tickets/recover_many?ids=1,2,3", {}
    )
    assert result == {"status": "ok"}


def test_recover_many_handles_none_response(http):
    http.put.return_value = None
    client = SuspendedTicketApiClient(http)
    assert client.recover_many(ids=[1]) == {}


def test_delete_calls_delete(http):
    client = SuspendedTicketApiClient(http)
    client.delete(id_=9)
    http.delete.assert_called_with("/api/v2/suspended_tickets/9")


def test_destroy_many_deletes_with_ids_query(http):
    http.delete.return_value = {"status": "ok"}
    client = SuspendedTicketApiClient(http)
    result = client.destroy_many(ids=[4, 5])
    http.delete.assert_called_with(
        "/api/v2/suspended_tickets/destroy_many?ids=4,5"
    )
    assert result == {"status": "ok"}


def test_destroy_many_handles_none_response(http):
    http.delete.return_value = None
    client = SuspendedTicketApiClient(http)
    assert client.destroy_many(ids=[1]) == {}


def test_list_attachments_returns_attachment_list(http, domain):
    http.get.return_value = {
        "attachments": [{"id": 1}, {"id": 2}]
    }
    client = SuspendedTicketApiClient(http)
    result = client.list_attachments(id_=7)
    http.get.assert_called_with("/api/v2/suspended_tickets/7/attachments")
    assert [r["id"] for r in result] == [1, 2]
    assert all(r["_cls"] == "Attachment" for r in result)


def test_list_attachments_handles_missing_key(http, domain):
    http.get.return_value = {}
    client = SuspendedTicketApiClient(http)
    assert client.list_attachments(id_=7) == []
