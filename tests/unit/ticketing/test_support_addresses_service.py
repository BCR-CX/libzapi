import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.support_address_cmds import (
    CreateSupportAddressCmd,
    UpdateSupportAddressCmd,
)
from libzapi.application.services.ticketing.support_addresses_service import (
    SupportAddressesService,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)


def _make_service(client=None):
    client = client or Mock()
    return SupportAddressesService(client), client


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.addresses
        assert service.list() is sentinel.addresses

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.address
        assert service.get(7) is sentinel.address
        client.get.assert_called_once_with(7)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(support_address_id=5)

    def test_verify_delegates(self):
        service, client = _make_service()
        client.verify.return_value = {"status": "ok"}
        assert service.verify(5) == {"status": "ok"}
        client.verify.assert_called_once_with(support_address_id=5)


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.address

        result = service.create(email="x@x", name="N", brand_id=1)

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateSupportAddressCmd)
        assert cmd.email == "x@x"
        assert cmd.name == "N"
        assert cmd.brand_id == 1
        assert result is sentinel.address


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.address

        result = service.update(7, name="N")

        assert client.update.call_args.kwargs["support_address_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateSupportAddressCmd)
        assert cmd.name == "N"
        assert result is sentinel.address

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.name is None
        assert cmd.brand_id is None
        assert cmd.default is None


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(email="x@x")

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list()
