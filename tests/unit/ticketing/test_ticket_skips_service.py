import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.ticket_skip_cmds import CreateTicketSkipCmd
from libzapi.application.services.ticketing.ticket_skips_service import (
    TicketSkipsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return TicketSkipsService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.skips
        assert service.list_all() is sentinel.skips
        client.list.assert_called_once_with()

    def test_list_by_user_delegates(self):
        service, client = _make_service()
        service.list_by_user(42)
        client.list_by_user.assert_called_once_with(user_id=42)

    def test_list_by_ticket_delegates(self):
        service, client = _make_service()
        service.list_by_ticket(7)
        client.list_by_ticket.assert_called_once_with(ticket_id=7)


class TestCreate:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.skip

        result = service.create(ticket_id=42, reason="not my area")

        call = client.create.call_args
        assert call.kwargs["ticket_id"] == 42
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, CreateTicketSkipCmd)
        assert cmd.reason == "not my area"
        assert result is sentinel.skip


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_create_propagates_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(ticket_id=1, reason="x")
