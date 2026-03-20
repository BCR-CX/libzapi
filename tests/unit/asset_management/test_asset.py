import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.asset_management.asset_api_client import AssetApiClient


MODULE = "libzapi.infrastructure.api_clients.asset_management.asset_api_client"
BASE = "/api/v2/it_asset_management/assets"


# ── list (GET, paginated) ──────────────────────────────────────────────


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"assets": [{}]}

    client = AssetApiClient(https)
    list(client.list())

    https.get.assert_called_with(BASE)


# ── get (GET) ───────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"asset": {"id": "abc123"}}

    client = AssetApiClient(https)
    client.get("abc123")

    https.get.assert_called_with(f"{BASE}/abc123")
    mock_to_domain.assert_called_once()


# ── create (POST) ──────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"asset": {"name": "Laptop"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"asset": {"id": "abc123", "name": "Laptop"}}

    client = AssetApiClient(https)
    client.create(mocker.Mock())

    https.post.assert_called_with(BASE, {"asset": {"name": "Laptop"}})
    mock_to_domain.assert_called_once()


# ── update (PATCH) ─────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"asset": {"name": "Updated"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"asset": {"id": "abc123", "name": "Updated"}}

    client = AssetApiClient(https)
    client.update("abc123", mocker.Mock())

    https.patch.assert_called_with(f"{BASE}/abc123", {"asset": {"name": "Updated"}})
    mock_to_domain.assert_called_once()


# ── delete (DELETE) ─────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = AssetApiClient(https)
    client.delete("abc123")

    https.delete.assert_called_with(f"{BASE}/abc123")


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

    client = AssetApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AssetApiClient(https)

    with pytest.raises(error_cls):
        client.get("abc123")


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_create_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"asset": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.side_effect = error_cls("error")

    client = AssetApiClient(https)

    with pytest.raises(error_cls):
        client.create(mocker.Mock())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_update_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"asset": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.side_effect = error_cls("error")

    client = AssetApiClient(https)

    with pytest.raises(error_cls):
        client.update("abc123", mocker.Mock())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.delete.side_effect = error_cls("error")

    client = AssetApiClient(https)

    with pytest.raises(error_cls):
        client.delete("abc123")
