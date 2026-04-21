import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.suspended_tickets_service import (
    SuspendedTicketsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return SuspendedTicketsService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list_all() is sentinel.items

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.item
        assert service.get_by_id(7) is sentinel.item
        client.get.assert_called_once_with(7)

    def test_recover_delegates(self):
        service, client = _make_service()
        client.recover.return_value = sentinel.item
        assert service.recover(7) is sentinel.item
        client.recover.assert_called_once_with(7)

    def test_recover_many_delegates(self):
        service, client = _make_service()
        client.recover_many.return_value = {"status": "ok"}
        assert service.recover_many([1, 2]) == {"status": "ok"}
        client.recover_many.assert_called_once_with([1, 2])

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(5)

    def test_destroy_many_delegates(self):
        service, client = _make_service()
        client.destroy_many.return_value = {"status": "ok"}
        assert service.destroy_many([1, 2]) == {"status": "ok"}
        client.destroy_many.assert_called_once_with([1, 2])

    def test_list_attachments_delegates(self):
        service, client = _make_service()
        client.list_attachments.return_value = sentinel.atts
        assert service.list_attachments(7) is sentinel.atts
        client.list_attachments.assert_called_once_with(7)


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_recover_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.recover.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.recover(1)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()
