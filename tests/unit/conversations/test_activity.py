import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.conversations.activity_api_client import ActivityApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.activity_api_client"


# ── post ────────────────────────────────────────────────────────────────


def test_post_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = ActivityApiClient(https)
    client.post("app-1", "conv-1", {"type": "business", "userId": "u-1"}, "typing:start")

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/activity",
        {"author": {"type": "business", "userId": "u-1"}, "type": "typing:start"},
    )


# ── error propagation: post ────────────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_post_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = ActivityApiClient(https)

    with pytest.raises(error_cls):
        client.post("app-1", "conv-1", {"type": "business"}, "typing:start")
