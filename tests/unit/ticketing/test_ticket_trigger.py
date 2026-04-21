import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.application.commands.ticketing.ticket_trigger_cmds import (
    CreateTicketTriggerCmd,
    UpdateTicketTriggerCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.ticketing.ticket_trigger import TicketTrigger
from libzapi.infrastructure.api_clients.ticketing import TicketTriggerApiClient


strategy = builds(
    TicketTrigger,
    raw_title=just("Trigger Test"),
)


@given(strategy)
def test_ticket_trigger_logical_key_from_raw_title(model: TicketTrigger):
    assert model.logical_key.as_str() == "ticket_trigger:trigger_test"


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_trigger_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


_ACTIONS = [{"field": "status", "value": "open"}]


# ---------------------------------------------------------------------------
# List/search iterator endpoints
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method_name, expected_path",
    [
        ("list", "/api/v2/triggers"),
        ("list_active", "/api/v2/triggers/active"),
    ],
)
def test_list_endpoints(method_name, expected_path, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"triggers": []}
    client = TicketTriggerApiClient(https)
    list(getattr(client, method_name)())
    https.get.assert_called_with(expected_path)


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "triggers": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketTriggerApiClient(http)
    result = list(client.list())
    assert len(result) == 2


def test_list_active_yields_items(http, domain):
    http.get.return_value = {
        "triggers": [{"id": 1}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketTriggerApiClient(http)
    assert len(list(client.list_active())) == 1


def test_search_yields_items(http, domain):
    http.get.return_value = {
        "triggers": [{"id": 7}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketTriggerApiClient(http)
    result = list(client.search(query="libzapi"))
    http.get.assert_called_with("/api/v2/triggers/search?query=libzapi")
    assert len(result) == 1


# ---------------------------------------------------------------------------
# Simple endpoints
# ---------------------------------------------------------------------------


def test_list_definitions_returns_dict(http):
    http.get.return_value = {"definitions": {"conditions": []}}
    client = TicketTriggerApiClient(http)
    assert client.list_definitions() == {"definitions": {"conditions": []}}
    http.get.assert_called_with("/api/v2/triggers/definitions")


def test_get_returns_domain(http, domain):
    http.get.return_value = {"trigger": {"id": 5}}
    client = TicketTriggerApiClient(http)
    result = client.get(trigger_id=5)
    http.get.assert_called_with("/api/v2/triggers/5")
    assert result["id"] == 5


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"trigger": {"id": 1, "title": "T"}}
    client = TicketTriggerApiClient(http)
    result = client.create(
        CreateTicketTriggerCmd(title="T", actions=_ACTIONS)
    )
    http.post.assert_called_with(
        "/api/v2/triggers", {"trigger": {"title": "T", "actions": _ACTIONS}}
    )
    assert result["title"] == "T"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"trigger": {"id": 1, "active": False}}
    client = TicketTriggerApiClient(http)
    client.update(trigger_id=1, entity=UpdateTicketTriggerCmd(active=False))
    http.put.assert_called_with(
        "/api/v2/triggers/1", {"trigger": {"active": False}}
    )


def test_delete_calls_delete(http):
    client = TicketTriggerApiClient(http)
    client.delete(trigger_id=7)
    http.delete.assert_called_with("/api/v2/triggers/7")


# ---------------------------------------------------------------------------
# Bulk operations
# ---------------------------------------------------------------------------


def test_create_many_posts_list(http, domain):
    http.post.return_value = {"job_status": {"id": "abc"}}
    client = TicketTriggerApiClient(http)
    client.create_many(
        [
            CreateTicketTriggerCmd(title="A", actions=_ACTIONS),
            CreateTicketTriggerCmd(title="B", actions=_ACTIONS),
        ]
    )
    http.post.assert_called_with(
        "/api/v2/triggers/create_many",
        {
            "triggers": [
                {"title": "A", "actions": _ACTIONS},
                {"title": "B", "actions": _ACTIONS},
            ]
        },
    )


def test_update_many_puts_bodies_with_ids(http, domain):
    http.put.return_value = {"job_status": {"id": "abc"}}
    client = TicketTriggerApiClient(http)
    client.update_many(
        [
            (1, UpdateTicketTriggerCmd(active=False)),
            (2, UpdateTicketTriggerCmd(description="n")),
        ]
    )
    http.put.assert_called_with(
        "/api/v2/triggers/update_many",
        {
            "triggers": [
                {"active": False, "id": 1},
                {"description": "n", "id": 2},
            ]
        },
    )


def test_destroy_many_deletes_with_ids(http, domain):
    http.delete.return_value = {"job_status": {"id": "abc"}}
    client = TicketTriggerApiClient(http)
    client.destroy_many([1, 2])
    http.delete.assert_called_with("/api/v2/triggers/destroy_many?ids=1,2")


def test_destroy_many_handles_none_response(http, domain):
    http.delete.return_value = None
    client = TicketTriggerApiClient(http)
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
    client = TicketTriggerApiClient(https)
    with pytest.raises(error_cls):
        list(client.list())
