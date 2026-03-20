import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.agent_availability.engagement_api_client import EngagementApiClient


MODULE = "libzapi.infrastructure.api_clients.agent_availability.engagement_api_client"
BASE = "/api/v2/engagements"


# ── list ────────────────────────────────────────────────────────────────


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [{"engagement_id": "eng-1"}]}

    client = EngagementApiClient(https)
    list(client.list())

    https.get.assert_called_with(BASE)


def test_list_with_filters_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": []}

    client = EngagementApiClient(https)
    list(client.list(agent_id=123, channel="Messaging"))

    https.get.assert_called_with(f"{BASE}?agent_id=123&channel=Messaging")


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": {"engagement_id": "eng-1"}}

    client = EngagementApiClient(https)
    client.get("eng-1")

    https.get.assert_called_with(f"{BASE}/eng-1")


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

    client = EngagementApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = EngagementApiClient(https)

    with pytest.raises(error_cls):
        client.get("eng-1")
