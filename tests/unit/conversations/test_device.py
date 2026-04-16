import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.device import Device
from libzapi.infrastructure.api_clients.conversations.device_api_client import DeviceApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.device_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(Device, id=just("dev-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "device:dev-1"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.return_value = {"devices": [{}]}

    client = DeviceApiClient(https)
    list(client.list_all("app-1", "usr-1"))

    https.get.assert_called_with("/v2/apps/app-1/users/usr-1/devices")


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.return_value = {"device": {}}

    client = DeviceApiClient(https)
    client.get("app-1", "usr-1", "dev-1")

    https.get.assert_called_with("/v2/apps/app-1/users/usr-1/devices/dev-1")


# ── error propagation: list_all (get) ──────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.side_effect = error_cls("error")

    client = DeviceApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("app-1", "usr-1"))


# ── error propagation: get ─────────────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.side_effect = error_cls("error")

    client = DeviceApiClient(https)

    with pytest.raises(error_cls):
        client.get("app-1", "usr-1", "dev-1")
