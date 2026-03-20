import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.asset_management.asset_field_api_client import AssetFieldApiClient


MODULE = "libzapi.infrastructure.api_clients.asset_management.asset_field_api_client"
BASE = "/api/v2/it_asset_management/asset_types"


# ── list (GET, paginated) ──────────────────────────────────────────────


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"fields": [{}]}

    client = AssetFieldApiClient(https)
    list(client.list("type-1"))

    https.get.assert_called_with(f"{BASE}/type-1/fields")


# ── get (GET) ───────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"field": {"id": 42}}

    client = AssetFieldApiClient(https)
    client.get("type-1", 42)

    https.get.assert_called_with(f"{BASE}/type-1/fields/42")
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

    client = AssetFieldApiClient(https)

    with pytest.raises(error_cls):
        list(client.list("type-1"))


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AssetFieldApiClient(https)

    with pytest.raises(error_cls):
        client.get("type-1", 42)
