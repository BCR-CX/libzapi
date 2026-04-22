import pytest

from libzapi.application.commands.ticketing.dynamic_content_cmds import (
    CreateDynamicContentItemCmd,
    CreateDynamicContentVariantCmd,
    UpdateDynamicContentItemCmd,
    UpdateDynamicContentVariantCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import DynamicContentApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.dynamic_content_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


class TestItems:
    def test_list_items_yields(self, http, domain):
        http.get.return_value = {
            "items": [{"id": 1}, {"id": 2}],
            "meta": {"has_more": False},
            "links": {"next": None},
        }
        client = DynamicContentApiClient(http)
        items = list(client.list_items())
        assert len(items) == 2
        assert all(i["_cls"] == "DynamicContentItem" for i in items)
        http.get.assert_called_with("/api/v2/dynamic_content/items")

    def test_get_item(self, http, domain):
        http.get.return_value = {"item": {"id": 7}}
        client = DynamicContentApiClient(http)
        result = client.get_item(7)
        assert result["_cls"] == "DynamicContentItem"
        http.get.assert_called_with("/api/v2/dynamic_content/items/7")

    def test_create_item(self, http, domain):
        http.post.return_value = {"item": {"id": 1}}
        client = DynamicContentApiClient(http)
        client.create_item(
            CreateDynamicContentItemCmd(name="greet", default_locale_id=1)
        )
        http.post.assert_called_with(
            "/api/v2/dynamic_content/items",
            {"item": {"name": "greet", "default_locale_id": 1, "variants": []}},
        )

    def test_update_item(self, http, domain):
        http.put.return_value = {"item": {"id": 7}}
        client = DynamicContentApiClient(http)
        client.update_item(7, UpdateDynamicContentItemCmd(name="x"))
        http.put.assert_called_with(
            "/api/v2/dynamic_content/items/7", {"item": {"name": "x"}}
        )

    def test_delete_item(self, http):
        client = DynamicContentApiClient(http)
        client.delete_item(7)
        http.delete.assert_called_with("/api/v2/dynamic_content/items/7")


class TestVariants:
    def test_list_variants(self, http, domain):
        http.get.return_value = {
            "variants": [{"id": 1}],
            "meta": {"has_more": False},
            "links": {"next": None},
        }
        client = DynamicContentApiClient(http)
        items = list(client.list_variants(7))
        assert len(items) == 1
        assert items[0]["_cls"] == "DynamicContentVariant"
        http.get.assert_called_with("/api/v2/dynamic_content/items/7/variants")

    def test_get_variant(self, http, domain):
        http.get.return_value = {"variant": {"id": 9}}
        client = DynamicContentApiClient(http)
        result = client.get_variant(7, 9)
        assert result["_cls"] == "DynamicContentVariant"
        http.get.assert_called_with("/api/v2/dynamic_content/items/7/variants/9")

    def test_create_variant(self, http, domain):
        http.post.return_value = {"variant": {"id": 9}}
        client = DynamicContentApiClient(http)
        client.create_variant(
            7, CreateDynamicContentVariantCmd(content="Hi", locale_id=1)
        )
        http.post.assert_called_with(
            "/api/v2/dynamic_content/items/7/variants",
            {"variant": {"content": "Hi", "locale_id": 1}},
        )

    def test_update_variant(self, http, domain):
        http.put.return_value = {"variant": {"id": 9}}
        client = DynamicContentApiClient(http)
        client.update_variant(
            7, 9, UpdateDynamicContentVariantCmd(content="new")
        )
        http.put.assert_called_with(
            "/api/v2/dynamic_content/items/7/variants/9",
            {"variant": {"content": "new"}},
        )

    def test_delete_variant(self, http):
        client = DynamicContentApiClient(http)
        client.delete_variant(7, 9)
        http.delete.assert_called_with("/api/v2/dynamic_content/items/7/variants/9")


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = DynamicContentApiClient(http)
    with pytest.raises(error_cls):
        list(client.list_items())


def test_logical_keys():
    from libzapi.domain.models.ticketing.dynamic_content import (
        DynamicContentItem,
        DynamicContentVariant,
    )

    item = DynamicContentItem(id=1, name="x", placeholder="{{x}}", default_locale_id=1)
    assert item.logical_key.as_str() == "dynamic_content_item:item_id_1"
    variant = DynamicContentVariant(id=9, content="Hi", locale_id=1)
    assert variant.logical_key.as_str() == "dynamic_content_variant:variant_id_9"
