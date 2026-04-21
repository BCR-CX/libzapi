from libzapi.application.commands.ticketing.brand_cmds import (
    CreateBrandCmd,
    UpdateBrandCmd,
)
from libzapi.infrastructure.mappers.ticketing.brand_mapper import (
    to_payload_create,
    to_payload_update,
)


def test_create_minimal_payload():
    payload = to_payload_create(CreateBrandCmd(name="Acme", subdomain="acme"))
    assert payload == {"brand": {"name": "Acme", "subdomain": "acme"}}


def test_create_with_all_optional_fields():
    cmd = CreateBrandCmd(
        name="Acme",
        subdomain="acme",
        active=True,
        host_mapping="help.acme.com",
        signature_template="sig",
        ticket_form_ids=[1, 2],
        brand_url="https://acme.com",
    )
    body = to_payload_create(cmd)["brand"]
    assert body == {
        "name": "Acme",
        "subdomain": "acme",
        "active": True,
        "host_mapping": "help.acme.com",
        "signature_template": "sig",
        "brand_url": "https://acme.com",
        "ticket_form_ids": [1, 2],
    }


def test_create_converts_iterable_to_list():
    cmd = CreateBrandCmd(name="Acme", subdomain="acme", ticket_form_ids=iter([1, 2]))
    body = to_payload_create(cmd)["brand"]
    assert body["ticket_form_ids"] == [1, 2]


def test_create_preserves_false_active():
    cmd = CreateBrandCmd(name="Acme", subdomain="acme", active=False)
    assert to_payload_create(cmd)["brand"]["active"] is False


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateBrandCmd()) == {"brand": {}}


def test_update_all_fields():
    cmd = UpdateBrandCmd(
        name="Acme",
        subdomain="acme",
        active=False,
        host_mapping="h",
        signature_template="s",
        ticket_form_ids=[9],
        brand_url="u",
        default=True,
    )
    assert to_payload_update(cmd) == {
        "brand": {
            "name": "Acme",
            "subdomain": "acme",
            "active": False,
            "host_mapping": "h",
            "signature_template": "s",
            "brand_url": "u",
            "ticket_form_ids": [9],
            "default": True,
        }
    }


def test_update_preserves_false_default():
    body = to_payload_update(UpdateBrandCmd(default=False))["brand"]
    assert body["default"] is False
