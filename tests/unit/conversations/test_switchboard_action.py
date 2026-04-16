import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.conversations.switchboard_action_api_client import SwitchboardActionApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.switchboard_action_api_client"


# ── accept_control ──────────────────────────────────────────────────────


def test_accept_control_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = SwitchboardActionApiClient(https)
    client.accept_control("app-1", "conv-1")

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/acceptControl",
        {},
    )


def test_accept_control_with_metadata(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = SwitchboardActionApiClient(https)
    client.accept_control("app-1", "conv-1", metadata={"key": "val"})

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/acceptControl",
        {"metadata": {"key": "val"}},
    )


# ── offer_control ──────────────────────────────────────────────────────


def test_offer_control_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_payload_offer_control", return_value={"integrationId": "int-1"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = SwitchboardActionApiClient(https)
    client.offer_control("app-1", "conv-1", mocker.Mock())

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/offerControl",
        {"integrationId": "int-1"},
    )


# ── pass_control ───────────────────────────────────────────────────────


def test_pass_control_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_payload_pass_control", return_value={"integrationId": "int-2"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = SwitchboardActionApiClient(https)
    client.pass_control("app-1", "conv-1", mocker.Mock())

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/passControl",
        {"integrationId": "int-2"},
    )


# ── release_control ────────────────────────────────────────────────────


def test_release_control_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = SwitchboardActionApiClient(https)
    client.release_control("app-1", "conv-1")

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/releaseControl",
        {},
    )


def test_release_control_with_metadata(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = SwitchboardActionApiClient(https)
    client.release_control("app-1", "conv-1", metadata={"key": "val"})

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/releaseControl",
        {"metadata": {"key": "val"}},
    )


# ── error propagation: accept_control (post) ──────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_accept_control_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = SwitchboardActionApiClient(https)

    with pytest.raises(error_cls):
        client.accept_control("app-1", "conv-1")
