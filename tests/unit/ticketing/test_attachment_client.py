import pytest

from libzapi.infrastructure.api_clients.ticketing.attachment_api_client import (
    AttachmentApiClient,
)


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.attachment_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


def test_get_reads_attachment_key(http, domain):
    http.get.return_value = {"attachment": {"id": 7}}
    client = AttachmentApiClient(http)
    result = client.get(attachment_id=7)
    http.get.assert_called_with("/api/v2/attachments/7")
    assert result["_cls"] == "Attachment"


def test_delete_calls_delete(http):
    client = AttachmentApiClient(http)
    client.delete(attachment_id=9)
    http.delete.assert_called_with("/api/v2/attachments/9")


def test_redact_puts_empty_body(http, domain):
    http.put.return_value = {"attachment": {"id": 9}}
    client = AttachmentApiClient(http)
    result = client.redact(attachment_id=9)
    http.put.assert_called_with("/api/v2/attachments/9/redact", {})
    assert result["_cls"] == "Attachment"


def test_upload_posts_multipart_with_filename(http, domain):
    http.post_multipart.return_value = {
        "upload": {
            "token": "abc",
            "attachment": {"id": 1},
            "attachments": [{"id": 1}],
        }
    }
    client = AttachmentApiClient(http)
    file = ("hello.txt", b"payload", "text/plain")
    result = client.upload(file=file)

    call = http.post_multipart.call_args
    assert call.args[0] == "/api/v2/uploads?filename=hello.txt"
    assert call.kwargs["files"] == {"uploaded_data": file}
    assert result["_cls"] == "Upload"
    assert result["token"] == "abc"


def test_upload_overrides_filename(http, domain):
    http.post_multipart.return_value = {
        "upload": {
            "token": "abc",
            "attachment": {"id": 1},
            "attachments": [{"id": 1}],
        }
    }
    client = AttachmentApiClient(http)
    file = ("hello.txt", b"x", "text/plain")
    client.upload(file=file, filename="override name.txt")
    call = http.post_multipart.call_args
    assert call.args[0] == "/api/v2/uploads?filename=override%20name.txt"


def test_upload_appends_token_to_existing_upload(http, domain):
    http.post_multipart.return_value = {
        "upload": {
            "token": "abc",
            "attachment": {"id": 2},
            "attachments": [{"id": 2}],
        }
    }
    client = AttachmentApiClient(http)
    client.upload(file=("b.bin", b"y"), token="abc")
    call = http.post_multipart.call_args
    assert call.args[0] == "/api/v2/uploads?filename=b.bin&token=abc"


def test_delete_upload_calls_delete_with_token(http):
    client = AttachmentApiClient(http)
    client.delete_upload(token="abc-def")
    http.delete.assert_called_with("/api/v2/uploads/abc-def")
