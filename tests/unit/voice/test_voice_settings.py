import pytest
from hypothesis import given
from hypothesis.strategies import builds

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.voice.voice_settings import VoiceSettings
from libzapi.infrastructure.api_clients.voice.voice_settings_api_client import VoiceSettingsApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.voice_settings_api_client"

strategy = builds(VoiceSettings)


@given(strategy)
def test_logical_key(model: VoiceSettings) -> None:
    assert model.logical_key.as_str() == "voice_settings:global"


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"settings": {}}
    client = VoiceSettingsApiClient(https)
    client.get()
    https.get.assert_called_with("/api/v2/channels/voice/settings")


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"settings": {"voice": True}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"settings": {}}
    client = VoiceSettingsApiClient(https)
    client.update(mocker.Mock())
    https.put.assert_called_with("/api/v2/channels/voice/settings", json={"settings": {"voice": True}})


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
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = VoiceSettingsApiClient(https)
    with pytest.raises(error_cls):
        client.get()


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_update_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"settings": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.side_effect = error_cls("error")
    client = VoiceSettingsApiClient(https)
    with pytest.raises(error_cls):
        client.update(mocker.Mock())
