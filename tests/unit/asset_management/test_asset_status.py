import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.asset_management.asset_status_api_client import AssetStatusApiClient


MODULE = "libzapi.infrastructure.api_clients.asset_management.asset_status_api_client"
BASE = "/api/v2/it_asset_management/statuses"


# ── list (GET, paginated) ──────────────────────────────────────────────


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"statuses": [{}]}

    client = AssetStatusApiClient(https)
    list(client.list())

    https.get.assert_called_with(BASE)


# ── get (GET) ───────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"status": {"id": "status-1"}}

    client = AssetStatusApiClient(https)
    client.get("status-1")

    https.get.assert_called_with(f"{BASE}/status-1")
    mock_to_domain.assert_called_once()


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

    client = AssetStatusApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AssetStatusApiClient(https)

    with pytest.raises(error_cls):
        client.get("status-1")
