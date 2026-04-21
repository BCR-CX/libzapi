import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.attachments_service import (
    AttachmentsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return AttachmentsService(client), client


class TestDelegation:
    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.att
        assert service.get(7) is sentinel.att
        client.get.assert_called_once_with(attachment_id=7)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(attachment_id=5)

    def test_redact_delegates(self):
        service, client = _make_service()
        client.redact.return_value = sentinel.att
        assert service.redact(5) is sentinel.att
        client.redact.assert_called_once_with(attachment_id=5)

    def test_upload_delegates(self):
        service, client = _make_service()
        client.upload.return_value = sentinel.upload
        file = ("f.txt", b"x", "text/plain")

        result = service.upload(file=file, filename="n", token="t")

        assert result is sentinel.upload
        client.upload.assert_called_once_with(
            file=file, filename="n", token="t"
        )

    def test_delete_upload_delegates(self):
        service, client = _make_service()
        service.delete_upload("abc")
        client.delete_upload.assert_called_once_with(token="abc")


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_upload_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.upload.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.upload(file=("f.txt", b"x"))

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_get_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.get.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.get(1)
