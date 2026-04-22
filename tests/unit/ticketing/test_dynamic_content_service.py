import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.dynamic_content_cmds import (
    CreateDynamicContentItemCmd,
    CreateDynamicContentVariantCmd,
    DynamicContentVariantInputCmd,
    UpdateDynamicContentItemCmd,
    UpdateDynamicContentVariantCmd,
)
from libzapi.application.services.ticketing.dynamic_content_service import (
    DynamicContentService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return DynamicContentService(client), client


class TestItemDelegation:
    def test_list_items_delegates(self):
        service, client = _make_service()
        client.list_items.return_value = sentinel.items
        assert service.list_items() is sentinel.items
        client.list_items.assert_called_once_with()

    def test_get_item_delegates(self):
        service, client = _make_service()
        service.get_item(7)
        client.get_item.assert_called_once_with(item_id=7)

    def test_delete_item_delegates(self):
        service, client = _make_service()
        service.delete_item(7)
        client.delete_item.assert_called_once_with(item_id=7)


class TestItemCreate:
    def test_minimal(self):
        service, client = _make_service()
        service.create_item(name="x", default_locale_id=1)
        cmd = client.create_item.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateDynamicContentItemCmd)
        assert cmd.name == "x"
        assert cmd.default_locale_id == 1
        assert cmd.variants == []

    def test_with_variants(self):
        service, client = _make_service()
        variants = [DynamicContentVariantInputCmd(content="Hi", locale_id=1)]
        service.create_item(name="x", default_locale_id=1, variants=variants)
        cmd = client.create_item.call_args.kwargs["entity"]
        assert len(cmd.variants) == 1


class TestItemUpdate:
    def test_update_item(self):
        service, client = _make_service()
        service.update_item(7, name="new")
        call = client.update_item.call_args
        assert call.kwargs["item_id"] == 7
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, UpdateDynamicContentItemCmd)
        assert cmd.name == "new"


class TestVariantDelegation:
    def test_list_variants_delegates(self):
        service, client = _make_service()
        service.list_variants(7)
        client.list_variants.assert_called_once_with(item_id=7)

    def test_get_variant_delegates(self):
        service, client = _make_service()
        service.get_variant(7, 9)
        client.get_variant.assert_called_once_with(item_id=7, variant_id=9)

    def test_delete_variant_delegates(self):
        service, client = _make_service()
        service.delete_variant(7, 9)
        client.delete_variant.assert_called_once_with(item_id=7, variant_id=9)


class TestVariantCreate:
    def test_builds_cmd(self):
        service, client = _make_service()
        service.create_variant(7, content="Hi", locale_id=1, default=True)
        call = client.create_variant.call_args
        assert call.kwargs["item_id"] == 7
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, CreateDynamicContentVariantCmd)
        assert cmd.content == "Hi"
        assert cmd.locale_id == 1
        assert cmd.default is True


class TestVariantUpdate:
    def test_builds_cmd(self):
        service, client = _make_service()
        service.update_variant(7, 9, content="x", active=False)
        call = client.update_variant.call_args
        assert call.kwargs["item_id"] == 7
        assert call.kwargs["variant_id"] == 9
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, UpdateDynamicContentVariantCmd)
        assert cmd.content == "x"
        assert cmd.active is False


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_items_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list_items.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_items()
