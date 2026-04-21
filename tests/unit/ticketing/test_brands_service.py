import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.brand_cmds import (
    CreateBrandCmd,
    UpdateBrandCmd,
)
from libzapi.application.services.ticketing.brands_service import BrandsService
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service():
    client = Mock()
    return BrandsService(client), client


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.brands
        assert service.list() is sentinel.brands

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.brand
        assert service.get(5) is sentinel.brand
        client.get.assert_called_once_with(brand_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(brand_id=5)

    def test_check_host_mapping_delegates(self):
        service, client = _make_service()
        client.check_host_mapping.return_value = {"ok": True}
        assert service.check_host_mapping("h", "s") == {"ok": True}
        client.check_host_mapping.assert_called_once_with(
            host_mapping="h", subdomain="s"
        )


class TestCreate:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.brand

        result = service.create(name="Acme", subdomain="acme", signature_template="sig")

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateBrandCmd)
        assert cmd.name == "Acme"
        assert cmd.subdomain == "acme"
        assert cmd.signature_template == "sig"
        assert result is sentinel.brand


class TestUpdate:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.brand

        result = service.update(7, signature_template="updated")

        call = client.update.call_args
        assert call.kwargs["brand_id"] == 7
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, UpdateBrandCmd)
        assert cmd.signature_template == "updated"
        assert result is sentinel.brand

    def test_empty_kwargs_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(7)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.name is None
        assert cmd.subdomain is None


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list()

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_create_propagates_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(name="A", subdomain="a")
