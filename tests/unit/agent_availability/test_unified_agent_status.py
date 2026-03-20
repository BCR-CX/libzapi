import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.agent_availability.unified_agent_status_api_client import (
    UnifiedAgentStatusApiClient,
)


MODULE = "libzapi.infrastructure.api_clients.agent_availability.unified_agent_status_api_client"
BASE = "/api/v2/agent_availabilities/agent_statuses"

STATUS_RESPONSE = {
    "default": [{"id": 3, "attributes": {"name": "Online", "description": "Agent is online"}}],
    "custom": [{"id": 100, "attributes": {"name": "Lunch", "description": "On break"}, "updated_at": "2024-01-01"}],
}


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = STATUS_RESPONSE

    client = UnifiedAgentStatusApiClient(https)
    client.list_all()

    https.get.assert_called_with(BASE)


# ── list_me ─────────────────────────────────────────────────────────────


def test_list_me_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = STATUS_RESPONSE

    client = UnifiedAgentStatusApiClient(https)
    client.list_me()

    https.get.assert_called_with(f"{BASE}/me")


# ── update_agent ────────────────────────────────────────────────────────


def test_update_agent_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"data": {}}

    client = UnifiedAgentStatusApiClient(https)
    client.update_agent(123, 3)

    https.put.assert_called_with(f"{BASE}/agents/123", {"id": 3})


# ── update_me ───────────────────────────────────────────────────────────


def test_update_me_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"data": {}}

    client = UnifiedAgentStatusApiClient(https)
    client.update_me(3)

    https.put.assert_called_with(f"{BASE}/agents/me", {"id": 3})


# ── bulk_update ─────────────────────────────────────────────────────────


def test_bulk_update_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"job_status": {}}

    client = UnifiedAgentStatusApiClient(https)
    client.bulk_update([1, 2, 3], 3)

    https.put.assert_called_with(f"{BASE}/agents/update_many?ids=1,2,3", {"id": 3})


# ── get_job_status ──────────────────────────────────────────────────────


def test_get_job_status_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"id": "job-1", "status": "completed"}

    client = UnifiedAgentStatusApiClient(https)
    client.get_job_status("job-1")

    https.get.assert_called_with(f"{BASE}/job_statuses/job-1")


# ── error propagation ──────────────────────────────────────────────────


ERROR_CLASSES = [
    pytest.param(Unauthorized, id="401"),
    pytest.param(NotFound, id="404"),
    pytest.param(UnprocessableEntity, id="422"),
    pytest.param(RateLimited, id="429"),
]


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = UnifiedAgentStatusApiClient(https)

    with pytest.raises(error_cls):
        client.list_all()


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_update_agent_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.side_effect = error_cls("error")

    client = UnifiedAgentStatusApiClient(https)

    with pytest.raises(error_cls):
        client.update_agent(123, 3)


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_job_status_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = UnifiedAgentStatusApiClient(https)

    with pytest.raises(error_cls):
        client.get_job_status("job-1")
