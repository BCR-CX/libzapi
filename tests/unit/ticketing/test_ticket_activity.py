import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import TicketActivityApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_activity_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


def test_list_no_filters(http, domain):
    http.get.return_value = {"activities": []}
    client = TicketActivityApiClient(http)
    list(client.list())
    http.get.assert_called_with("/api/v2/activities")


def test_list_with_since(http, domain):
    http.get.return_value = {"activities": []}
    client = TicketActivityApiClient(http)
    list(client.list(since="2026-04-21T00:00:00Z"))
    http.get.assert_called_with(
        "/api/v2/activities?since=2026-04-21T00%3A00%3A00Z"
    )


def test_list_with_include(http, domain):
    http.get.return_value = {"activities": []}
    client = TicketActivityApiClient(http)
    list(client.list(include="users"))
    http.get.assert_called_with("/api/v2/activities?include=users")


def test_list_with_both_filters(http, domain):
    http.get.return_value = {"activities": []}
    client = TicketActivityApiClient(http)
    list(client.list(since="2026-04-21", include="users"))
    http.get.assert_called_with(
        "/api/v2/activities?since=2026-04-21&include=users"
    )


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "activities": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketActivityApiClient(http)
    items = list(client.list())
    assert len(items) == 2
    assert all(i["_cls"] == "TicketActivity" for i in items)


def test_get_calls_endpoint(http, domain):
    http.get.return_value = {"activity": {"id": 5}}
    client = TicketActivityApiClient(http)
    client.get(activity_id=5)
    http.get.assert_called_with("/api/v2/activities/5")


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = TicketActivityApiClient(http)
    with pytest.raises(error_cls):
        list(client.list())


def test_ticket_activity_logical_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.ticket_activity import TicketActivity

    act = TicketActivity(
        id=7,
        verb="tickets.assignment",
        title="Assigned",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert act.logical_key.as_str() == "ticket_activity:activity_id_7"
