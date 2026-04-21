import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.view_cmds import (
    CreateViewCmd,
    UpdateViewCmd,
)
from libzapi.application.services.ticketing.views_service import ViewsService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


def _make_service(client=None):
    client = client or Mock()
    return ViewsService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list_all.return_value = sentinel.views
        assert service.list_all() is sentinel.views

    def test_list_active_delegates(self):
        service, client = _make_service()
        client.list_active.return_value = sentinel.views
        assert service.list_active() is sentinel.views

    def test_search_delegates(self):
        service, client = _make_service()
        client.search.return_value = sentinel.matches
        assert service.search(query="foo") is sentinel.matches
        client.search.assert_called_once_with(query="foo")

    def test_count_delegates(self):
        service, client = _make_service()
        client.count.return_value = sentinel.count
        assert service.count() is sentinel.count

    def test_count_view_delegates(self):
        service, client = _make_service()
        client.count_view.return_value = {"value": 7}
        assert service.count_view(5) == {"value": 7}
        client.count_view.assert_called_once_with(view_id=5)

    def test_count_many_delegates(self):
        service, client = _make_service()
        client.count_many.return_value = [{"view_id": 1, "value": 2}]
        assert service.count_many([1, 2]) == [{"view_id": 1, "value": 2}]
        client.count_many.assert_called_once_with(view_ids=[1, 2])

    def test_execute_delegates(self):
        service, client = _make_service()
        client.execute.return_value = {"rows": []}
        assert service.execute(5) == {"rows": []}
        client.execute.assert_called_once_with(view_id=5)

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.view
        assert service.get_by_id(5) is sentinel.view
        client.get.assert_called_once_with(view_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(view_id=5)

    def test_destroy_many_delegates(self):
        service, client = _make_service()
        client.destroy_many.return_value = sentinel.job
        assert service.destroy_many([1, 2]) is sentinel.job
        client.destroy_many.assert_called_once_with(view_ids=[1, 2])


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.view
        result = service.create(title="V")
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateViewCmd)
        assert cmd.title == "V"
        assert result is sentinel.view

    def test_passes_all_optional_fields(self):
        service, client = _make_service()
        service.create(
            title="V",
            all=[{"field": "s", "operator": "is", "value": "o"}],
            any=[{"field": "p", "operator": "is", "value": "u"}],
            description="d",
            active=False,
            position=2,
            output={"columns": ["subject"]},
            restriction={"type": "Group", "id": 1},
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.active is False
        assert cmd.position == 2
        assert cmd.output == {"columns": ["subject"]}
        assert cmd.restriction == {"type": "Group", "id": 1}


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.view
        result = service.update(7, description="updated", active=False)
        assert client.update.call_args.kwargs["view_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateViewCmd)
        assert cmd.description == "updated"
        assert cmd.active is False
        assert result is sentinel.view

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.title is None
        assert cmd.active is None


class TestUpdateMany:
    def test_pairs_ids_with_update_cmds(self):
        service, client = _make_service()
        client.update_many.return_value = sentinel.job
        result = service.update_many(
            [(1, {"active": False}), (2, {"description": "n"})]
        )
        pairs = client.update_many.call_args.kwargs["updates"]
        assert pairs[0][0] == 1
        assert isinstance(pairs[0][1], UpdateViewCmd)
        assert pairs[0][1].active is False
        assert pairs[1][1].description == "n"
        assert result is sentinel.job

    def test_empty_updates(self):
        service, client = _make_service()
        service.update_many([])
        assert client.update_many.call_args.kwargs["updates"] == []


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(title="t")

    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_update_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.update.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.update(1)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_all_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list_all.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()
