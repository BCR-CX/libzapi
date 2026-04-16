import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.voice.recording_api_client import RecordingApiClient


def test_delete_all_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = RecordingApiClient(https)
    client.delete_all(1)
    https.delete.assert_called_with("/api/v2/channels/voice/calls/1/recordings")


def test_delete_by_type_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = RecordingApiClient(https)
    client.delete_by_type(1, "call")
    https.delete.assert_called_with("/api/v2/channels/voice/calls/1/recordings/call")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_delete_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.delete.side_effect = error_cls("error")
    client = RecordingApiClient(https)
    with pytest.raises(error_cls):
        client.delete_all(1)
