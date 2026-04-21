import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.ticket_trigger_cmds import (
    CreateTicketTriggerCmd,
    UpdateTicketTriggerCmd,
)
from libzapi.application.services.ticketing.ticket_trigger_service import (
    TicketTriggerService,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


_ACTIONS = [{"field": "status", "value": "open"}]


def _make_service(client=None):
    client = client or Mock()
    return TicketTriggerService(client), client


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.triggers
        assert service.list() is sentinel.triggers

    def test_list_active_delegates(self):
        service, client = _make_service()
        client.list_active.return_value = sentinel.triggers
        assert service.list_active() is sentinel.triggers

    def test_search_delegates(self):
        service, client = _make_service()
        client.search.return_value = sentinel.matches
        assert service.search(query="foo") is sentinel.matches
        client.search.assert_called_once_with(query="foo")

    def test_list_definitions_delegates(self):
        service, client = _make_service()
        client.list_definitions.return_value = {"conditions": []}
        assert service.list_definitions() == {"conditions": []}

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.trigger
        assert service.get(5) is sentinel.trigger
        client.get.assert_called_once_with(trigger_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(trigger_id=5)

    def test_destroy_many_delegates(self):
        service, client = _make_service()
        client.destroy_many.return_value = sentinel.job
        assert service.destroy_many([1, 2]) is sentinel.job
        client.destroy_many.assert_called_once_with(trigger_ids=[1, 2])


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.trigger
        result = service.create(title="T", actions=_ACTIONS)
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateTicketTriggerCmd)
        assert cmd.title == "T"
        assert cmd.actions == _ACTIONS
        assert result is sentinel.trigger

    def test_passes_all_optional_fields(self):
        service, client = _make_service()
        service.create(
            title="T",
            actions=_ACTIONS,
            conditions={"all": []},
            active=False,
            description="d",
            category_id="1",
            position=3,
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.conditions == {"all": []}
        assert cmd.active is False
        assert cmd.description == "d"
        assert cmd.category_id == "1"
        assert cmd.position == 3


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.trigger
        result = service.update(7, description="updated", active=False)
        assert client.update.call_args.kwargs["trigger_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateTicketTriggerCmd)
        assert cmd.description == "updated"
        assert cmd.active is False
        assert result is sentinel.trigger

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.title is None
        assert cmd.active is None


class TestCreateMany:
    def test_converts_dicts_to_create_cmds(self):
        service, client = _make_service()
        client.create_many.return_value = sentinel.job
        result = service.create_many(
            [
                {"title": "A", "actions": _ACTIONS},
                {"title": "B", "actions": _ACTIONS, "active": True},
            ]
        )
        entities = client.create_many.call_args.kwargs["entities"]
        assert len(entities) == 2
        assert all(isinstance(c, CreateTicketTriggerCmd) for c in entities)
        assert entities[1].active is True
        assert result is sentinel.job

    def test_empty_input(self):
        service, client = _make_service()
        service.create_many([])
        assert client.create_many.call_args.kwargs["entities"] == []


class TestUpdateMany:
    def test_pairs_ids_with_update_cmds(self):
        service, client = _make_service()
        client.update_many.return_value = sentinel.job
        result = service.update_many(
            [(1, {"active": False}), (2, {"description": "n"})]
        )
        pairs = client.update_many.call_args.kwargs["updates"]
        assert pairs[0][0] == 1
        assert isinstance(pairs[0][1], UpdateTicketTriggerCmd)
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
            service.create(title="t", actions=_ACTIONS)

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
