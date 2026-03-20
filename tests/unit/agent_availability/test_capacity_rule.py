import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.agent_availability.capacity_rule_api_client import CapacityRuleApiClient


MODULE = "libzapi.infrastructure.api_clients.agent_availability.capacity_rule_api_client"
BASE = "/api/v2/capacity/rules"


# ── list ────────────────────────────────────────────────────────────────


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [{"id": "rule-1", "name": "Default"}]}

    client = CapacityRuleApiClient(https)
    list(client.list())

    https.get.assert_called_with(BASE)


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": {"id": "rule-1"}}

    client = CapacityRuleApiClient(https)
    client.get("rule-1")

    https.get.assert_called_with(f"{BASE}/rule-1")


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"name": "Test"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"data": {"id": "rule-1", "name": "Test"}}

    client = CapacityRuleApiClient(https)
    client.create(mocker.Mock())

    https.post.assert_called_with(BASE, {"name": "Test"})


# ── update ──────────────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"name": "Updated"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"data": {"id": "rule-1", "name": "Updated"}}

    client = CapacityRuleApiClient(https)
    client.update("rule-1", mocker.Mock())

    https.put.assert_called_with(f"{BASE}/rule-1", {"name": "Updated"})


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = CapacityRuleApiClient(https)
    client.delete("rule-1")

    https.delete.assert_called_with(f"{BASE}/rule-1")


# ── assign_agents ───────────────────────────────────────────────────────


def test_assign_agents_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {}

    client = CapacityRuleApiClient(https)
    client.assign_agents("rule-1", [1, 2, 3])

    https.patch.assert_called_with(f"{BASE}/rule-1/agents", {"agents": [1, 2, 3]})


# ── list_assignees ──────────────────────────────────────────────────────


def test_list_assignees_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"assignees": [{"agent_id": 1}]}

    client = CapacityRuleApiClient(https)
    list(client.list_assignees())

    https.get.assert_called_with(f"{BASE}/assignees")


def test_list_rule_assignees_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"assignees": [{"agent_id": 1}]}

    client = CapacityRuleApiClient(https)
    list(client.list_rule_assignees("rule-1"))

    https.get.assert_called_with(f"{BASE}/rule-1/assignees")


# ── error propagation ──────────────────────────────────────────────────


ERROR_CLASSES = [
    pytest.param(Unauthorized, id="401"),
    pytest.param(NotFound, id="404"),
    pytest.param(UnprocessableEntity, id="422"),
    pytest.param(RateLimited, id="429"),
]


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_list_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CapacityRuleApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CapacityRuleApiClient(https)

    with pytest.raises(error_cls):
        client.get("rule-1")


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_create_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_create", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.side_effect = error_cls("error")

    client = CapacityRuleApiClient(https)

    with pytest.raises(error_cls):
        client.create(mocker.Mock())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_update_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_update", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.side_effect = error_cls("error")

    client = CapacityRuleApiClient(https)

    with pytest.raises(error_cls):
        client.update("rule-1", mocker.Mock())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.delete.side_effect = error_cls("error")

    client = CapacityRuleApiClient(https)

    with pytest.raises(error_cls):
        client.delete("rule-1")
