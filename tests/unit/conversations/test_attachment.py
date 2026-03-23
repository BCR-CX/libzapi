import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.attachment import Attachment
from libzapi.infrastructure.api_clients.conversations.attachment_api_client import AttachmentApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.attachment_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(Attachment, mediaUrl=just("https://cdn.example.com/file.png"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "sunco_attachment:https://cdn.example.com/file.png"


# ── upload (multipart) ─────────────────────────────────────────────────


def test_upload_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post_multipart.return_value = {"attachment": {}}

    client = AttachmentApiClient(https)
    file_tuple = ("image.png", b"content", "image/png")
    client.upload("app-1", file_tuple)

    https.post_multipart.assert_called_with(
        "/v2/apps/app-1/attachments",
        files={"source": file_tuple},
    )


# ── delete (POST to /remove) ──────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = AttachmentApiClient(https)
    client.delete("app-1", "https://cdn.example.com/file.png")

    https.post.assert_called_with(
        "/v2/apps/app-1/attachments/remove",
        {"mediaUrl": "https://cdn.example.com/file.png"},
    )


# ── error propagation: upload (post_multipart) ────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_upload_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post_multipart.side_effect = error_cls("error")

    client = AttachmentApiClient(https)

    with pytest.raises(error_cls):
        client.upload("app-1", ("image.png", b"content", "image/png"))


# ── error propagation: delete (post) ──────────────────────────────────


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
    https.post.side_effect = error_cls("error")

    client = AttachmentApiClient(https)

    with pytest.raises(error_cls):
        client.delete("app-1", "https://cdn.example.com/file.png")
