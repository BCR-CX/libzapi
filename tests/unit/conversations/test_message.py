import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.message import Message
from libzapi.infrastructure.api_clients.conversations.message_api_client import MessageApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.message_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(Message, id=just("msg-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "message:msg-1"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.return_value = {"messages": [{}]}

    client = MessageApiClient(https)
    list(client.list_all("app-1", "conv-1"))

    https.get_raw.assert_called_with(
        "https://example.zendesk.com/sc/v2/apps/app-1/conversations/conv-1/messages?page[size]=100"
    )


# ── post ────────────────────────────────────────────────────────────────


def test_post_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"author": {}, "content": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {"message": {}}

    client = MessageApiClient(https)
    client.post("app-1", "conv-1", mocker.Mock())

    https.post.assert_called_with(
        "/v2/apps/app-1/conversations/conv-1/messages",
        {"author": {}, "content": {}},
    )


# ── delete_all ──────────────────────────────────────────────────────────


def test_delete_all_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = MessageApiClient(https)
    client.delete_all("app-1", "conv-1")

    https.delete.assert_called_with("/v2/apps/app-1/conversations/conv-1/messages")


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = MessageApiClient(https)
    client.delete("app-1", "conv-1", "msg-1")

    https.delete.assert_called_with("/v2/apps/app-1/conversations/conv-1/messages/msg-1")


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
    https.get_raw.side_effect = error_cls("error")

    client = MessageApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("app-1", "conv-1"))


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
    mocker.patch(f"{MODULE}.to_payload_create", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = MessageApiClient(https)

    with pytest.raises(error_cls):
        client.post("app-1", "conv-1", mocker.Mock())


# ── error propagation: delete ──────────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.delete.side_effect = error_cls("error")

    client = MessageApiClient(https)

    with pytest.raises(error_cls):
        client.delete("app-1", "conv-1", "msg-1")
