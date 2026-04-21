import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.sessions_service import (
    SessionsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return SessionsService(client), client


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list() is sentinel.items

    def test_list_user_delegates(self):
        service, client = _make_service()
        client.list_user.return_value = sentinel.items
        assert service.list_user(5) is sentinel.items
        client.list_user.assert_called_once_with(user_id=5)

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.session
        assert service.get(5, 7) is sentinel.session
        client.get.assert_called_once_with(user_id=5, session_id=7)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5, 7)
        client.delete.assert_called_once_with(user_id=5, session_id=7)

    def test_delete_user_sessions_delegates(self):
        service, client = _make_service()
        service.delete_user_sessions(5)
        client.delete_user_sessions.assert_called_once_with(user_id=5)

    def test_get_current_delegates(self):
        service, client = _make_service()
        client.get_current.return_value = sentinel.session
        assert service.get_current() is sentinel.session

    def test_logout_current_delegates(self):
        service, client = _make_service()
        service.logout_current()
        client.logout_current.assert_called_once_with()


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list()

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_get_current_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.get_current.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.get_current()
