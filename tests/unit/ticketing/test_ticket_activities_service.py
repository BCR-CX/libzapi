import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.ticket_activities_service import (
    TicketActivitiesService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return TicketActivitiesService(client), client


class TestList:
    def test_list_all_no_filters(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list_all() is sentinel.items
        client.list.assert_called_once_with(since=None, include=None)

    def test_list_all_with_filters(self):
        service, client = _make_service()
        service.list_all(since="2026-04-21", include="users")
        client.list.assert_called_once_with(since="2026-04-21", include="users")


class TestGet:
    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.activity
        assert service.get_by_id(5) is sentinel.activity
        client.get.assert_called_once_with(activity_id=5)


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()
