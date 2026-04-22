import pytest

from libzapi.application.commands.ticketing.custom_ticket_status_cmds import (
    CreateCustomTicketStatusCmd,
    UpdateCustomTicketStatusCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import CustomTicketStatusApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.custom_ticket_status_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_list_no_filters(http, domain):
    http.get.return_value = {"custom_statuses": []}
    client = CustomTicketStatusApiClient(http)
    list(client.list())
    http.get.assert_called_with("/api/v2/custom_statuses")


def test_list_with_status_categories(http, domain):
    http.get.return_value = {"custom_statuses": []}
    client = CustomTicketStatusApiClient(http)
    list(client.list(status_categories=["open", "pending"]))
    http.get.assert_called_with(
        "/api/v2/custom_statuses?status_categories=open%2Cpending"
    )


def test_list_with_active_filter(http, domain):
    http.get.return_value = {"custom_statuses": []}
    client = CustomTicketStatusApiClient(http)
    list(client.list(active=True))
    http.get.assert_called_with("/api/v2/custom_statuses?active=true")


def test_list_with_active_false(http, domain):
    http.get.return_value = {"custom_statuses": []}
    client = CustomTicketStatusApiClient(http)
    list(client.list(active=False))
    http.get.assert_called_with("/api/v2/custom_statuses?active=false")


def test_list_with_default_filter(http, domain):
    http.get.return_value = {"custom_statuses": []}
    client = CustomTicketStatusApiClient(http)
    list(client.list(default=True))
    http.get.assert_called_with("/api/v2/custom_statuses?default=true")


def test_list_with_default_false(http, domain):
    http.get.return_value = {"custom_statuses": []}
    client = CustomTicketStatusApiClient(http)
    list(client.list(default=False))
    http.get.assert_called_with("/api/v2/custom_statuses?default=false")


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "custom_statuses": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = CustomTicketStatusApiClient(http)
    assert len(list(client.list())) == 2


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


def test_get_calls_endpoint(http, domain):
    http.get.return_value = {"custom_status": {"id": 5}}
    client = CustomTicketStatusApiClient(http)
    client.get(status_id=5)
    http.get.assert_called_with("/api/v2/custom_statuses/5")


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"custom_status": {"id": 1}}
    client = CustomTicketStatusApiClient(http)
    client.create(
        CreateCustomTicketStatusCmd(status_category="open", agent_label="Busy")
    )
    http.post.assert_called_with(
        "/api/v2/custom_statuses",
        {"custom_status": {"status_category": "open", "agent_label": "Busy"}},
    )


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


def test_update_puts_payload(http, domain):
    http.put.return_value = {"custom_status": {"id": 7}}
    client = CustomTicketStatusApiClient(http)
    client.update(status_id=7, entity=UpdateCustomTicketStatusCmd(agent_label="New"))
    http.put.assert_called_with(
        "/api/v2/custom_statuses/7",
        {"custom_status": {"agent_label": "New"}},
    )


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = CustomTicketStatusApiClient(http)
    with pytest.raises(error_cls):
        list(client.list())


# ---------------------------------------------------------------------------
# Domain logical key
# ---------------------------------------------------------------------------


def test_custom_ticket_status_logical_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.custom_ticket_status import (
        CustomTicketStatus,
    )

    status = CustomTicketStatus(
        id=42,
        status_category="open",
        agent_label="Being worked",
        end_user_label="In progress",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert status.logical_key.as_str() == "custom_ticket_status:status_id_42"
