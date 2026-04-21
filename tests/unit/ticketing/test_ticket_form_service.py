import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.ticket_form_cmds import (
    CreateTicketFormCmd,
    UpdateTicketFormCmd,
)
from libzapi.application.services.ticketing.ticket_forms_service import (
    TicketFormsService,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)


def _make_service(client=None):
    client = client or Mock()
    return TicketFormsService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.forms
        assert service.list_all() is sentinel.forms

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.form
        assert service.get_by_id(5) is sentinel.form
        client.get.assert_called_once_with(ticket_form_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(ticket_form_id=5)

    def test_clone_delegates(self):
        service, client = _make_service()
        client.clone.return_value = sentinel.form
        assert service.clone(5) is sentinel.form
        client.clone.assert_called_once_with(ticket_form_id=5)

    def test_reorder_delegates(self):
        service, client = _make_service()
        service.reorder([3, 1, 2])
        client.reorder.assert_called_once_with(ticket_form_ids=[3, 1, 2])


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.form

        result = service.create(name="F", ticket_field_ids=[1])

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateTicketFormCmd)
        assert cmd.name == "F"
        assert cmd.ticket_field_ids == [1]
        assert result is sentinel.form

    def test_passes_all_optional_fields(self):
        service, client = _make_service()
        service.create(
            name="F",
            ticket_field_ids=[1],
            display_name="Public",
            end_user_visible=False,
            in_all_brands=True,
            restricted_brand_ids=[9],
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.display_name == "Public"
        assert cmd.end_user_visible is False
        assert cmd.in_all_brands is True
        assert cmd.restricted_brand_ids == [9]


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.form

        result = service.update(7, name="Updated", active=False)

        assert client.update.call_args.kwargs["ticket_form_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateTicketFormCmd)
        assert cmd.name == "Updated"
        assert cmd.active is False
        assert result is sentinel.form

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.name is None
        assert cmd.ticket_field_ids is None


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(name="n", ticket_field_ids=[1])

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
