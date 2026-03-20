import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.agent_availability.agent_availability_api_client import (
    AgentAvailabilityApiClient,
)


MODULE = "libzapi.infrastructure.api_clients.agent_availability.agent_availability_api_client"
BASE = "/api/v2/agent_availabilities"

JSONAPI_RESPONSE = {
    "data": [
        {
            "id": "123",
            "type": "agent_availabilities",
            "attributes": {"agent_id": 123, "group_ids": [1], "skills": [], "version": 1},
            "relationships": {"channels": {"data": [{"id": "123:support", "type": "channels"}]}},
        }
    ],
    "included": [
        {
            "id": "123:support",
            "type": "channels",
            "attributes": {"name": "support", "status": "online", "work_item_count": 2},
        }
    ],
}

JSONAPI_SINGLE = {
    "data": {
        "id": "123",
        "type": "agent_availabilities",
        "attributes": {"agent_id": 123, "group_ids": [1], "skills": [], "version": 1},
        "relationships": {"channels": {"data": []}},
    },
    "included": [],
}


# ── list ────────────────────────────────────────────────────────────────


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = JSONAPI_RESPONSE

    client = AgentAvailabilityApiClient(https)
    list(client.list())

    https.get.assert_called_with(BASE)


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = JSONAPI_SINGLE

    client = AgentAvailabilityApiClient(https)
    client.get(123)

    https.get.assert_called_with(f"{BASE}/123")


# ── get_me ──────────────────────────────────────────────────────────────


def test_get_me_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = JSONAPI_SINGLE

    client = AgentAvailabilityApiClient(https)
    client.get_me()

    https.get.assert_called_with(f"{BASE}/me")


# ── work_items ──────────────────────────────────────────────────────────


def test_work_items_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [{"id": "wi-1", "type": "work_items", "attributes": {"added_at": "2024-01-01"}}]}

    client = AgentAvailabilityApiClient(https)
    list(client.work_items(123, "support"))

    https.get.assert_called_with(f"{BASE}/123/channels/support/relationships/work_items")


# ── my_work_items ───────────────────────────────────────────────────────


def test_my_work_items_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": []}

    client = AgentAvailabilityApiClient(https)
    list(client.my_work_items("messaging"))

    https.get.assert_called_with(f"{BASE}/me/channels/messaging/relationships/work_items")


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

    client = AgentAvailabilityApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AgentAvailabilityApiClient(https)

    with pytest.raises(error_cls):
        client.get(123)


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_me_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AgentAvailabilityApiClient(https)

    with pytest.raises(error_cls):
        client.get_me()


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_work_items_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AgentAvailabilityApiClient(https)

    with pytest.raises(error_cls):
        list(client.work_items(123, "support"))


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_my_work_items_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AgentAvailabilityApiClient(https)

    with pytest.raises(error_cls):
        list(client.my_work_items("support"))
