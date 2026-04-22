from libzapi.application.commands.ticketing.dynamic_content_cmds import (
    CreateDynamicContentItemCmd,
    CreateDynamicContentVariantCmd,
    DynamicContentVariantInputCmd,
    UpdateDynamicContentItemCmd,
    UpdateDynamicContentVariantCmd,
)
from libzapi.infrastructure.mappers.ticketing.dynamic_content_mapper import (
    to_payload_create_item,
    to_payload_create_variant,
    to_payload_update_item,
    to_payload_update_variant,
)


def test_create_item_minimal():
    payload = to_payload_create_item(
        CreateDynamicContentItemCmd(name="greeting", default_locale_id=1)
    )
    assert payload == {
        "item": {"name": "greeting", "default_locale_id": 1, "variants": []}
    }


def test_create_item_with_variants():
    payload = to_payload_create_item(
        CreateDynamicContentItemCmd(
            name="greeting",
            default_locale_id=1,
            variants=[
                DynamicContentVariantInputCmd(
                    content="Hello", locale_id=1, default=True, active=True
                ),
                DynamicContentVariantInputCmd(content="Olá", locale_id=77),
            ],
        )
    )
    assert payload == {
        "item": {
            "name": "greeting",
            "default_locale_id": 1,
            "variants": [
                {
                    "content": "Hello",
                    "locale_id": 1,
                    "default": True,
                    "active": True,
                },
                {"content": "Olá", "locale_id": 77},
            ],
        }
    }


def test_update_item_empty():
    assert to_payload_update_item(UpdateDynamicContentItemCmd()) == {"item": {}}


def test_update_item_with_name():
    assert to_payload_update_item(UpdateDynamicContentItemCmd(name="x")) == {
        "item": {"name": "x"}
    }


def test_create_variant_minimal():
    payload = to_payload_create_variant(
        CreateDynamicContentVariantCmd(content="Hi", locale_id=1)
    )
    assert payload == {"variant": {"content": "Hi", "locale_id": 1}}


def test_create_variant_full():
    payload = to_payload_create_variant(
        CreateDynamicContentVariantCmd(
            content="Hi", locale_id=1, default=False, active=True
        )
    )
    assert payload == {
        "variant": {
            "content": "Hi",
            "locale_id": 1,
            "default": False,
            "active": True,
        }
    }


def test_update_variant_empty():
    assert to_payload_update_variant(UpdateDynamicContentVariantCmd()) == {
        "variant": {}
    }


def test_update_variant_all_fields():
    payload = to_payload_update_variant(
        UpdateDynamicContentVariantCmd(
            content="x", locale_id=1, default=True, active=False
        )
    )
    assert payload == {
        "variant": {
            "content": "x",
            "locale_id": 1,
            "default": True,
            "active": False,
        }
    }
