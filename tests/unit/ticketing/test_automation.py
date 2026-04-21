import pytest

from libzapi.application.commands.ticketing.automation_cmds import (
    CreateAutomationCmd,
    UpdateAutomationCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import AutomationApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.automation_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


_ACTIONS = [{"field": "status", "value": "closed"}]
_CONDS = {"all": [], "any": []}


# ---------------------------------------------------------------------------
# List/search iterator endpoints
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method_name, expected_path",
    [
        ("list_all", "/api/v2/automations"),
        ("list_active", "/api/v2/automations/active"),
    ],
)
def test_list_endpoints(method_name, expected_path, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"automations": []}
    client = AutomationApiClient(https)
    list(getattr(client, method_name)())
    https.get.assert_called_with(expected_path)


def test_list_all_yields_items(http, domain):
    http.get.return_value = {
        "automations": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = AutomationApiClient(http)
    assert len(list(client.list_all())) == 2


def test_list_active_yields_items(http, domain):
    http.get.return_value = {
        "automations": [{"id": 1}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = AutomationApiClient(http)
    assert len(list(client.list_active())) == 1


def test_search_yields_items(http, domain):
    http.get.return_value = {
        "automations": [{"id": 3}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = AutomationApiClient(http)
    result = list(client.search(query="libzapi"))
    http.get.assert_called_with("/api/v2/automations/search?query=libzapi")
    assert len(result) == 1


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


def test_automation_logical_key_normalises_title():
    from datetime import datetime

    from libzapi.domain.models.ticketing.automation import Automation

    auto = Automation(
        id=1,
        url="https://x",
        title="Close Old",
        active=True,
        updated_at=datetime.now(),
        created_at=datetime.now(),
        default=False,
        actions=[],
        conditions=None,  # type: ignore[arg-type]
        position=1,
        raw_title="Close Old Tickets",
    )
    assert auto.logical_key.as_str() == "automation:close_old_tickets"


def test_get_returns_domain(http, domain):
    http.get.return_value = {"automation": {"id": 42}}
    client = AutomationApiClient(http)
    result = client.get(automation_id=42)
    http.get.assert_called_with("/api/v2/automations/42")
    assert result["id"] == 42


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"automation": {"id": 1}}
    client = AutomationApiClient(http)
    client.create(
        CreateAutomationCmd(title="A", actions=_ACTIONS, conditions=_CONDS)
    )
    http.post.assert_called_with(
        "/api/v2/automations",
        {
            "automation": {
                "title": "A",
                "actions": _ACTIONS,
                "conditions": _CONDS,
            }
        },
    )


def test_update_puts_payload(http, domain):
    http.put.return_value = {"automation": {"id": 1, "active": False}}
    client = AutomationApiClient(http)
    client.update(automation_id=1, entity=UpdateAutomationCmd(active=False))
    http.put.assert_called_with(
        "/api/v2/automations/1", {"automation": {"active": False}}
    )


def test_delete_calls_delete(http):
    client = AutomationApiClient(http)
    client.delete(automation_id=7)
    http.delete.assert_called_with("/api/v2/automations/7")


# ---------------------------------------------------------------------------
# Bulk operations
# ---------------------------------------------------------------------------


def test_create_many_posts_list(http, domain):
    http.post.return_value = {"job_status": {"id": "abc"}}
    client = AutomationApiClient(http)
    client.create_many(
        [
            CreateAutomationCmd(title="A", actions=_ACTIONS, conditions=_CONDS),
            CreateAutomationCmd(title="B", actions=_ACTIONS, conditions=_CONDS),
        ]
    )
    http.post.assert_called_with(
        "/api/v2/automations/create_many",
        {
            "automations": [
                {"title": "A", "actions": _ACTIONS, "conditions": _CONDS},
                {"title": "B", "actions": _ACTIONS, "conditions": _CONDS},
            ]
        },
    )


def test_update_many_puts_bodies_with_ids(http, domain):
    http.put.return_value = {"job_status": {"id": "abc"}}
    client = AutomationApiClient(http)
    client.update_many(
        [
            (1, UpdateAutomationCmd(active=False)),
            (2, UpdateAutomationCmd(title="n")),
        ]
    )
    http.put.assert_called_with(
        "/api/v2/automations/update_many",
        {
            "automations": [
                {"active": False, "id": 1},
                {"title": "n", "id": 2},
            ]
        },
    )


def test_destroy_many_deletes_with_ids(http, domain):
    http.delete.return_value = {"job_status": {"id": "abc"}}
    client = AutomationApiClient(http)
    client.destroy_many([1, 2])
    http.delete.assert_called_with(
        "/api/v2/automations/destroy_many?ids=1,2"
    )


def test_destroy_many_handles_none_response(http, domain):
    http.delete.return_value = None
    client = AutomationApiClient(http)
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
    client = AutomationApiClient(https)
    with pytest.raises(error_cls):
        list(client.list_all())
