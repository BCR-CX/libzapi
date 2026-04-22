import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized
from libzapi.infrastructure.api_clients.ticketing import IncrementalExportApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.incremental_export_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# Time-based: tickets / users / organizations / ticket_events
# ---------------------------------------------------------------------------


def test_tickets_hits_expected_path(http, domain):
    http.get.return_value = {"tickets": []}
    client = IncrementalExportApiClient(http)
    list(client.tickets(start_time=123))
    http.get.assert_called_with("/api/v2/incremental/tickets?start_time=123")


def test_tickets_yields_items(http, domain):
    http.get.return_value = {
        "tickets": [{"id": 1}, {"id": 2}],
        "next_page": None,
        "end_time": 500,
    }
    client = IncrementalExportApiClient(http)
    items = list(client.tickets(start_time=100))
    assert len(items) == 2
    assert all(i["_cls"] == "Ticket" for i in items)


def test_ticket_events_returns_raw_dicts(http, domain):
    http.get.return_value = {
        "ticket_events": [{"id": 1, "child_events": []}]
    }
    client = IncrementalExportApiClient(http)
    items = list(client.ticket_events(start_time=100))
    assert items == [{"id": 1, "child_events": []}]
    http.get.assert_called_with(
        "/api/v2/incremental/ticket_events?start_time=100"
    )


def test_users_hits_expected_path(http, domain):
    http.get.return_value = {"users": [{"id": 1}]}
    client = IncrementalExportApiClient(http)
    items = list(client.users(start_time=500))
    assert len(items) == 1
    assert items[0]["_cls"] == "User"
    http.get.assert_called_with("/api/v2/incremental/users?start_time=500")


def test_organizations_hits_expected_path(http, domain):
    http.get.return_value = {"organizations": [{"id": 1}]}
    client = IncrementalExportApiClient(http)
    items = list(client.organizations(start_time=500))
    assert len(items) == 1
    assert items[0]["_cls"] == "Organization"
    http.get.assert_called_with(
        "/api/v2/incremental/organizations?start_time=500"
    )


def test_start_time_coerced_to_int(http, domain):
    http.get.return_value = {"tickets": []}
    client = IncrementalExportApiClient(http)
    list(client.tickets(start_time="42"))  # type: ignore[arg-type]
    http.get.assert_called_with("/api/v2/incremental/tickets?start_time=42")


# ---------------------------------------------------------------------------
# Cursor-based: tickets_cursor / users_cursor
# ---------------------------------------------------------------------------


def test_tickets_cursor_stops_on_end_of_stream(http, domain):
    http.get.return_value = {
        "tickets": [{"id": 1}],
        "end_of_stream": True,
        "after_url": "https://example.zendesk.com/api/v2/incremental/tickets/cursor?cursor=abc",
    }
    client = IncrementalExportApiClient(http)
    items = list(client.tickets_cursor(start_time=100))
    assert len(items) == 1
    http.get.assert_called_once_with(
        "/api/v2/incremental/tickets/cursor?start_time=100"
    )


def test_tickets_cursor_follows_after_url_https(http, domain):
    http.get.side_effect = [
        {
            "tickets": [{"id": 1}],
            "after_url": "https://example.zendesk.com/api/v2/incremental/tickets/cursor?cursor=abc",
            "end_of_stream": False,
        },
        {
            "tickets": [{"id": 2}],
            "after_url": None,
            "end_of_stream": True,
        },
    ]
    client = IncrementalExportApiClient(http)
    items = list(client.tickets_cursor(start_time=100))
    assert len(items) == 2
    assert http.get.call_count == 2
    assert http.get.call_args_list[1].args == (
        "/api/v2/incremental/tickets/cursor?cursor=abc",
    )


def test_cursor_stops_when_after_url_missing(http, domain):
    http.get.return_value = {"tickets": [{"id": 1}], "end_of_stream": False}
    client = IncrementalExportApiClient(http)
    items = list(client.tickets_cursor(start_time=100))
    assert len(items) == 1


def test_users_cursor_hits_expected_path(http, domain):
    http.get.return_value = {"users": [], "end_of_stream": True}
    client = IncrementalExportApiClient(http)
    list(client.users_cursor(start_time=42))
    http.get.assert_called_once_with(
        "/api/v2/incremental/users/cursor?start_time=42"
    )


def test_cursor_handles_relative_after_url(http, domain):
    http.get.side_effect = [
        {
            "tickets": [{"id": 1}],
            "after_url": "/api/v2/incremental/tickets/cursor?cursor=xyz",
            "end_of_stream": False,
        },
        {"tickets": [], "end_of_stream": True},
    ]
    client = IncrementalExportApiClient(http)
    list(client.tickets_cursor(start_time=100))
    assert http.get.call_args_list[1].args == (
        "/api/v2/incremental/tickets/cursor?cursor=xyz",
    )


def test_cursor_skips_when_items_missing(http, domain):
    http.get.return_value = {"end_of_stream": True}
    client = IncrementalExportApiClient(http)
    items = list(client.tickets_cursor(start_time=100))
    assert items == []


# ---------------------------------------------------------------------------
# Sample
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "resource", ["tickets", "users", "organizations", "ticket_events"]
)
def test_sample_hits_expected_path(resource, http):
    http.get.return_value = {"count": 1}
    client = IncrementalExportApiClient(http)
    assert client.sample(resource=resource, start_time=99) == {"count": 1}
    http.get.assert_called_with(
        f"/api/v2/incremental/{resource}/sample?start_time=99"
    )


def test_sample_raises_on_unknown_resource(http):
    client = IncrementalExportApiClient(http)
    with pytest.raises(ValueError):
        client.sample(resource="articles", start_time=100)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, RateLimited])
def test_tickets_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = IncrementalExportApiClient(http)
    with pytest.raises(error_cls):
        list(client.tickets(start_time=100))


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, RateLimited])
def test_cursor_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = IncrementalExportApiClient(http)
    with pytest.raises(error_cls):
        list(client.tickets_cursor(start_time=100))
