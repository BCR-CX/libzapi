import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.custom_ticket_status_cmds import (
    CreateCustomTicketStatusCmd,
    UpdateCustomTicketStatusCmd,
)
from libzapi.application.services.ticketing.custom_ticket_statuses_service import (
    CustomTicketStatusesService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return CustomTicketStatusesService(client), client


class TestList:
    def test_list_all_no_filters(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list_all() is sentinel.items
        client.list.assert_called_once_with(
            status_categories=None, active=None, default=None
        )

    def test_list_all_with_filters(self):
        service, client = _make_service()
        service.list_all(status_categories=["open"], active=True, default=False)
        client.list.assert_called_once_with(
            status_categories=["open"], active=True, default=False
        )


class TestGet:
    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.status
        assert service.get_by_id(5) is sentinel.status
        client.get.assert_called_once_with(status_id=5)


class TestCreate:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.status

        result = service.create(
            status_category="open",
            agent_label="Working",
            end_user_label="In progress",
        )

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateCustomTicketStatusCmd)
        assert cmd.status_category == "open"
        assert cmd.agent_label == "Working"
        assert cmd.end_user_label == "In progress"
        assert result is sentinel.status

    def test_accepts_active_flag(self):
        service, client = _make_service()
        service.create(status_category="open", agent_label="x", active=True)
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.active is True


class TestUpdate:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.status

        result = service.update(status_id=7, agent_label="New label")

        call = client.update.call_args
        assert call.kwargs["status_id"] == 7
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, UpdateCustomTicketStatusCmd)
        assert cmd.agent_label == "New label"
        assert result is sentinel.status

    def test_empty_update(self):
        service, client = _make_service()
        service.update(status_id=7)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.agent_label is None
        assert cmd.end_user_label is None
        assert cmd.description is None
        assert cmd.end_user_description is None
        assert cmd.active is None


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
            service.create(status_category="open", agent_label="x")
