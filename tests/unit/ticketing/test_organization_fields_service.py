import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.organization_field_cmds import (
    CreateOrganizationFieldCmd,
    OrganizationFieldOptionCmd,
    UpdateOrganizationFieldCmd,
)
from libzapi.application.services.ticketing.organization_fields_service import (
    OrganizationFieldsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return OrganizationFieldsService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list_all.return_value = sentinel.items
        assert service.list_all() is sentinel.items
        client.list_all.assert_called_once_with()

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        service.get_by_id(7)
        client.get.assert_called_once_with(organization_field_id=7)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(7)
        client.delete.assert_called_once_with(organization_field_id=7)

    def test_reorder_delegates(self):
        service, client = _make_service()
        service.reorder([1, 2])
        client.reorder.assert_called_once_with(organization_field_ids=[1, 2])

    def test_list_options_delegates(self):
        service, client = _make_service()
        service.list_options(7)
        client.list_options.assert_called_once_with(organization_field_id=7)

    def test_get_option_by_id_delegates(self):
        service, client = _make_service()
        service.get_option_by_id(7, 9)
        client.get_option.assert_called_once_with(
            organization_field_id=7, option_id=9
        )

    def test_delete_option_delegates(self):
        service, client = _make_service()
        service.delete_option(7, 9)
        client.delete_option.assert_called_once_with(
            organization_field_id=7, option_id=9
        )


class TestCreateUpdate:
    def test_create_builds_cmd(self):
        service, client = _make_service()
        service.create(key="k", type="text", title="t")
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateOrganizationFieldCmd)
        assert cmd.key == "k"
        assert cmd.type == "text"
        assert cmd.title == "t"

    def test_update_builds_cmd(self):
        service, client = _make_service()
        service.update(7, title="new", position=3)
        call = client.update.call_args
        assert call.kwargs["organization_field_id"] == 7
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, UpdateOrganizationFieldCmd)
        assert cmd.title == "new"
        assert cmd.position == 3


class TestUpsertOption:
    def test_builds_cmd(self):
        service, client = _make_service()
        service.upsert_option(7, name="A", value="a")
        call = client.upsert_option.call_args
        assert call.kwargs["organization_field_id"] == 7
        option = call.kwargs["option"]
        assert isinstance(option, OrganizationFieldOptionCmd)
        assert option.name == "A"
        assert option.value == "a"
        assert option.id is None

    def test_with_id(self):
        service, client = _make_service()
        service.upsert_option(7, name="A", value="a", id=9)
        option = client.upsert_option.call_args.kwargs["option"]
        assert option.id == 9


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list_all.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()
