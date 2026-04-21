import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def test_upload_and_delete_upload(ticketing: Ticketing):
    suffix = _unique()
    filename = f"libzapi-{suffix}.txt"
    upload = ticketing.attachments.upload(
        file=(filename, b"libzapi integration test", "text/plain")
    )
    try:
        assert upload.token
        assert upload.attachment.file_name == filename
    finally:
        ticketing.attachments.delete_upload(upload.token)


def test_upload_append_to_existing_token(ticketing: Ticketing):
    suffix = _unique()
    first = ticketing.attachments.upload(
        file=(f"first-{suffix}.txt", b"one", "text/plain")
    )
    try:
        second = ticketing.attachments.upload(
            file=(f"second-{suffix}.txt", b"two", "text/plain"),
            token=first.token,
        )
        assert second.token == first.token
        assert len(second.attachments) >= 2
    finally:
        ticketing.attachments.delete_upload(first.token)
