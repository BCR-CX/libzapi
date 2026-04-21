import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.macro_cmds import (
    CreateMacroCmd,
    UpdateMacroCmd,
)
from libzapi.application.services.ticketing.macro_service import MacroService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_BASIC_ACTIONS = [{"field": "status", "value": "solved"}]


def _make_service(client=None):
    client = client or Mock()
    return MacroService(client), client


# ---------------------------------------------------------------------------
# Delegation-only methods
# ---------------------------------------------------------------------------


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.macros
        assert service.list() is sentinel.macros
        client.list.assert_called_once_with()

    def test_list_active_delegates(self):
        service, client = _make_service()
        client.list_active.return_value = sentinel.macros
        assert service.list_active() is sentinel.macros

    def test_search_delegates(self):
        service, client = _make_service()
        client.search.return_value = sentinel.matches
        assert service.search(query="foo") is sentinel.matches
        client.search.assert_called_once_with(query="foo")

    def test_list_categories_delegates(self):
        service, client = _make_service()
        client.list_categories.return_value = ["a", "b"]
        assert service.list_categories() == ["a", "b"]

    def test_list_definitions_delegates(self):
        service, client = _make_service()
        client.list_definitions.return_value = {"x": 1}
        assert service.list_definitions() == {"x": 1}

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.macro
        assert service.get(5) is sentinel.macro
        client.get.assert_called_once_with(macro_id=5)

    def test_apply_delegates(self):
        service, client = _make_service()
        client.apply.return_value = {"ticket": {"id": 1}}
        assert service.apply(5) == {"ticket": {"id": 1}}
        client.apply.assert_called_once_with(macro_id=5)

    def test_apply_to_ticket_delegates(self):
        service, client = _make_service()
        client.apply_to_ticket.return_value = {"ticket": {"id": 7}}
        assert service.apply_to_ticket(ticket_id=7, macro_id=5) == {
            "ticket": {"id": 7}
        }
        client.apply_to_ticket.assert_called_once_with(ticket_id=7, macro_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(macro_id=5)

    def test_destroy_many_delegates(self):
        service, client = _make_service()
        client.destroy_many.return_value = sentinel.job
        assert service.destroy_many([1, 2]) is sentinel.job
        client.destroy_many.assert_called_once_with(macro_ids=[1, 2])


# ---------------------------------------------------------------------------
# create / update
# ---------------------------------------------------------------------------


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.macro

        result = service.create(title="Close", actions=_BASIC_ACTIONS)

        client.create.assert_called_once()
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateMacroCmd)
        assert cmd.title == "Close"
        assert cmd.actions == _BASIC_ACTIONS
        assert result is sentinel.macro

    def test_passes_all_optional_fields(self):
        service, client = _make_service()
        service.create(
            title="Close",
            actions=_BASIC_ACTIONS,
            active=False,
            description="d",
            restriction={"type": "Group", "id": 1},
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.active is False
        assert cmd.description == "d"
        assert cmd.restriction == {"type": "Group", "id": 1}


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.macro

        result = service.update(7, description="updated", active=False)

        client.update.assert_called_once()
        assert client.update.call_args.kwargs["macro_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateMacroCmd)
        assert cmd.description == "updated"
        assert cmd.active is False
        assert result is sentinel.macro

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.title is None
        assert cmd.actions is None
        assert cmd.active is None


# ---------------------------------------------------------------------------
# create_many / update_many
# ---------------------------------------------------------------------------


class TestCreateMany:
    def test_converts_dicts_to_create_cmds(self):
        service, client = _make_service()
        client.create_many.return_value = sentinel.job

        result = service.create_many(
            [
                {"title": "A", "actions": _BASIC_ACTIONS},
                {"title": "B", "actions": _BASIC_ACTIONS, "active": True},
            ]
        )

        entities = client.create_many.call_args.kwargs["entities"]
        assert len(entities) == 2
        assert all(isinstance(c, CreateMacroCmd) for c in entities)
        assert entities[0].title == "A"
        assert entities[1].title == "B"
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
        assert isinstance(pairs[0][1], UpdateMacroCmd)
        assert pairs[0][1].active is False
        assert pairs[1][0] == 2
        assert pairs[1][1].description == "n"
        assert result is sentinel.job

    def test_empty_updates(self):
        service, client = _make_service()
        service.update_many([])
        assert client.update_many.call_args.kwargs["updates"] == []


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(title="t", actions=_BASIC_ACTIONS)

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
