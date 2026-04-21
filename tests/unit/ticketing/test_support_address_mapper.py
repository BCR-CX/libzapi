from libzapi.application.commands.ticketing.support_address_cmds import (
    CreateSupportAddressCmd,
    UpdateSupportAddressCmd,
)
from libzapi.infrastructure.mappers.ticketing.support_address_mapper import (
    to_payload_create,
    to_payload_update,
)


def test_create_minimal_payload():
    payload = to_payload_create(CreateSupportAddressCmd(email="hi@x.com"))
    assert payload == {"recipient_address": {"email": "hi@x.com"}}


def test_create_includes_all_optionals():
    payload = to_payload_create(
        CreateSupportAddressCmd(
            email="hi@x.com", name="Support", brand_id=3, default=False
        )
    )
    assert payload == {
        "recipient_address": {
            "email": "hi@x.com",
            "name": "Support",
            "brand_id": 3,
            "default": False,
        }
    }


def test_create_preserves_false_default():
    payload = to_payload_create(
        CreateSupportAddressCmd(email="hi@x.com", default=False)
    )
    assert payload["recipient_address"]["default"] is False


def test_update_empty_patch():
    assert to_payload_update(UpdateSupportAddressCmd()) == {
        "recipient_address": {}
    }


def test_update_includes_fields():
    payload = to_payload_update(
        UpdateSupportAddressCmd(name="N", brand_id=1, default=True)
    )
    assert payload == {
        "recipient_address": {"name": "N", "brand_id": 1, "default": True}
    }


def test_update_preserves_false_default():
    payload = to_payload_update(UpdateSupportAddressCmd(default=False))
    assert payload["recipient_address"]["default"] is False
