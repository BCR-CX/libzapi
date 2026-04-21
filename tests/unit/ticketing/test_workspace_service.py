import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.workspace_cmds import (
    CreateWorkspaceCmd,
    UpdateWorkspaceCmd,
)
from libzapi.application.services.ticketing.workspace_service import WorkspaceService
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)


_COND = {"all": [{"field": "status", "operator": "is", "value": "new"}]}


def _make_service(client=None):
    client = client or Mock()
    return WorkspaceService(client), client


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.ws
        assert service.list() is sentinel.ws

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.ws
        assert service.get(5) is sentinel.ws
        client.get.assert_called_once_with(workspace_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(workspace_id=5)

    def test_destroy_many_delegates(self):
        service, client = _make_service()
        service.destroy_many([1, 2])
        client.destroy_many.assert_called_once_with(workspace_ids=[1, 2])

    def test_reorder_delegates(self):
        service, client = _make_service()
        service.reorder([3, 1, 2])
        client.reorder.assert_called_once_with(workspace_ids=[3, 1, 2])


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.ws

        result = service.create(title="W", conditions=_COND)

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateWorkspaceCmd)
        assert cmd.title == "W"
        assert cmd.conditions == _COND
        assert result is sentinel.ws


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.ws

        result = service.update(7, title="N", activated=False)

        assert client.update.call_args.kwargs["workspace_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateWorkspaceCmd)
        assert cmd.title == "N"
        assert cmd.activated is False
        assert result is sentinel.ws

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.title is None
        assert cmd.conditions is None


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(title="t", conditions=_COND)

    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_update_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.update.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.update(1)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list()
