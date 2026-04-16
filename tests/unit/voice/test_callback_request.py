import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.voice.callback_request_api_client import CallbackRequestApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.callback_request_api_client"


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"callback_request": {"phone": "+1"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"callback_request": {}}
    client = CallbackRequestApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with(
        "/api/v2/channels/voice/callback_requests", json={"callback_request": {"phone": "+1"}}
    )


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_create_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"callback_request": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.side_effect = error_cls("error")
    client = CallbackRequestApiClient(https)
    with pytest.raises(error_cls):
        client.create(mocker.Mock())
