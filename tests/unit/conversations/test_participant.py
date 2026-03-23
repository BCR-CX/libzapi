import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.participant import Participant
from libzapi.infrastructure.api_clients.conversations.participant_api_client import ParticipantApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.participant_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(Participant, id=just("part-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "participant:part-1"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.return_value = {"participants": [{}]}

    client = ParticipantApiClient(https)
    list(client.list_all("app-1", "conv-1"))

    https.get.assert_called_with("/v2/apps/app-1/conversations/conv-1/participants")


# ── join ────────────────────────────────────────────────────────────────


def test_join_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = ParticipantApiClient(https)
    client.join("app-1", "conv-1", "user-1")

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/participants/join",
        {"userId": "user-1"},
    )


# ── leave ───────────────────────────────────────────────────────────────


def test_leave_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = ParticipantApiClient(https)
    client.leave("app-1", "conv-1", "user-1")

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/participants/leave",
        {"userId": "user-1"},
    )


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

    client = ParticipantApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("app-1", "conv-1"))


# ── error propagation: join (post) ────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_join_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = ParticipantApiClient(https)

    with pytest.raises(error_cls):
        client.join("app-1", "conv-1", "user-1")
