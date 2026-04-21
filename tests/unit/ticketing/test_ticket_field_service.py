import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.ticket_field_cmds import (
    CreateTicketFieldCmd,
    TicketFieldOptionCmd,
    UpdateTicketFieldCmd,
)
from libzapi.application.services.ticketing.ticket_fields_service import (
    TicketFieldsService,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)


def _make_service(client=None):
    client = client or Mock()
    return TicketFieldsService(client), client


# ---------------------------------------------------------------------------
# Delegation-only methods
# ---------------------------------------------------------------------------


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.fields
        assert service.list_all() is sentinel.fields
        client.list.assert_called_once_with()

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.field
        assert service.get_by_id(5) is sentinel.field
        client.get.assert_called_once_with(field_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(field_id=5)

    def test_reorder_delegates(self):
        service, client = _make_service()
        service.reorder([3, 1, 2])
        client.reorder.assert_called_once_with(field_ids=[3, 1, 2])

    def test_list_options_delegates(self):
        service, client = _make_service()
        client.list_options.return_value = sentinel.options
        assert service.list_options(5) is sentinel.options
        client.list_options.assert_called_once_with(field_id=5)

    def test_get_option_delegates(self):
        service, client = _make_service()
        client.get_option.return_value = sentinel.option
        assert service.get_option(field_id=5, option_id=7) is sentinel.option
        client.get_option.assert_called_once_with(field_id=5, option_id=7)

    def test_delete_option_delegates(self):
        service, client = _make_service()
        service.delete_option(field_id=5, option_id=7)
        client.delete_option.assert_called_once_with(field_id=5, option_id=7)


# ---------------------------------------------------------------------------
# create / update
# ---------------------------------------------------------------------------


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.field

        result = service.create(title="Order", type="text")

        client.create.assert_called_once()
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateTicketFieldCmd)
        assert cmd.title == "Order"
        assert cmd.type == "text"
        assert result is sentinel.field

    def test_passes_all_optional_fields(self):
        service, client = _make_service()
        service.create(
            title="Order",
            type="tagger",
            active=False,
            required=True,
            description="d",
            custom_field_options=[{"name": "A", "value": "a"}],
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.active is False
        assert cmd.required is True
        assert cmd.description == "d"
        assert cmd.custom_field_options == [{"name": "A", "value": "a"}]


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.field

        result = service.update(7, description="updated", active=False)

        client.update.assert_called_once()
        assert client.update.call_args.kwargs["field_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateTicketFieldCmd)
        assert cmd.description == "updated"
        assert cmd.active is False
        assert result is sentinel.field

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.title is None
        assert cmd.active is None


# ---------------------------------------------------------------------------
# upsert_option
# ---------------------------------------------------------------------------


class TestUpsertOption:
    def test_builds_option_cmd_and_delegates(self):
        service, client = _make_service()
        client.upsert_option.return_value = sentinel.option

        result = service.upsert_option(field_id=5, name="A", value="a")

        assert result is sentinel.option
        assert client.upsert_option.call_args.kwargs["field_id"] == 5
        cmd = client.upsert_option.call_args.kwargs["option"]
        assert isinstance(cmd, TicketFieldOptionCmd)
        assert cmd.name == "A"
        assert cmd.value == "a"
        assert cmd.id is None

    def test_passes_id(self):
        service, client = _make_service()
        service.upsert_option(field_id=5, name="A", value="a", id=9)
        cmd = client.upsert_option.call_args.kwargs["option"]
        assert cmd.id == 9


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
            service.create(title="t", type="text")

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
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()
