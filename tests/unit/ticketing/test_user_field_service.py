import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.user_field_cmds import (
    CreateUserFieldCmd,
    UpdateUserFieldCmd,
    UserFieldOptionCmd,
)
from libzapi.application.services.ticketing.user_fields_service import (
    UserFieldsService,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)


def _make_service(client=None):
    client = client or Mock()
    return UserFieldsService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list_all.return_value = sentinel.fields
        assert service.list_all() is sentinel.fields

    def test_list_options_delegates(self):
        service, client = _make_service()
        client.list_options.return_value = sentinel.options
        assert service.list_options(5) is sentinel.options
        client.list_options.assert_called_once_with(user_field_id=5)

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.field
        assert service.get_by_id(5) is sentinel.field
        client.get.assert_called_once_with(user_field_id=5)

    def test_get_option_by_id_delegates(self):
        service, client = _make_service()
        client.get_option.return_value = sentinel.option
        assert (
            service.get_option_by_id(user_field_id=5, user_field_option_id=7)
            is sentinel.option
        )
        client.get_option.assert_called_once_with(
            user_field_id=5, user_field_option_id=7
        )

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(user_field_id=5)

    def test_reorder_delegates(self):
        service, client = _make_service()
        service.reorder([3, 1, 2])
        client.reorder.assert_called_once_with(user_field_ids=[3, 1, 2])

    def test_delete_option_delegates(self):
        service, client = _make_service()
        service.delete_option(user_field_id=5, user_field_option_id=7)
        client.delete_option.assert_called_once_with(
            user_field_id=5, user_field_option_id=7
        )


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.field

        result = service.create(key="region", type="text", title="Region")

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateUserFieldCmd)
        assert cmd.key == "region"
        assert cmd.type == "text"
        assert cmd.title == "Region"
        assert result is sentinel.field


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.field

        result = service.update(7, title="New", active=False)

        assert client.update.call_args.kwargs["user_field_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateUserFieldCmd)
        assert cmd.title == "New"
        assert cmd.active is False
        assert result is sentinel.field

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.title is None
        assert cmd.active is None


class TestUpsertOption:
    def test_builds_option_cmd_and_delegates(self):
        service, client = _make_service()
        client.upsert_option.return_value = sentinel.option

        result = service.upsert_option(user_field_id=5, name="A", value="a")

        assert result is sentinel.option
        cmd = client.upsert_option.call_args.kwargs["option"]
        assert isinstance(cmd, UserFieldOptionCmd)
        assert cmd.name == "A"
        assert cmd.value == "a"
        assert cmd.id is None

    def test_passes_id(self):
        service, client = _make_service()
        service.upsert_option(user_field_id=5, name="A", value="a", id=9)
        cmd = client.upsert_option.call_args.kwargs["option"]
        assert cmd.id == 9


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(key="k", type="text", title="T")

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
