from libzapi.application.commands.ticketing.organization_cmds import (
    CreateOrganizationCmd,
    UpdateOrganizationCmd,
)
from libzapi.infrastructure.mappers.ticketing.organization_mapper import (
    to_payload_create,
    to_payload_update,
)


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_name():
    payload = to_payload_create(CreateOrganizationCmd(name="Acme"))
    assert payload == {"organization": {"name": "Acme"}}


def test_create_includes_all_optional_fields():
    cmd = CreateOrganizationCmd(
        name="Acme",
        domain_names=["acme.com", "acme.org"],
        details="details",
        notes="notes",
        group_id=10,
        shared_tickets=True,
        shared_comments=False,
        tags=["vip", "priority"],
        organization_fields={"industry": "tech"},
        external_id="ext-1",
    )

    body = to_payload_create(cmd)["organization"]

    assert body["name"] == "Acme"
    assert body["domain_names"] == ["acme.com", "acme.org"]
    assert body["details"] == "details"
    assert body["notes"] == "notes"
    assert body["group_id"] == 10
    assert body["shared_tickets"] is True
    assert body["shared_comments"] is False
    assert body["tags"] == ["vip", "priority"]
    assert body["organization_fields"] == {"industry": "tech"}
    assert body["external_id"] == "ext-1"


def test_create_converts_iterables_to_lists():
    cmd = CreateOrganizationCmd(
        name="Acme",
        domain_names=iter(["a.com", "b.com"]),
        tags=iter(["x", "y"]),
    )
    body = to_payload_create(cmd)["organization"]
    assert body["domain_names"] == ["a.com", "b.com"]
    assert body["tags"] == ["x", "y"]


def test_create_preserves_false_booleans():
    cmd = CreateOrganizationCmd(
        name="Acme", shared_tickets=False, shared_comments=False
    )
    body = to_payload_create(cmd)["organization"]
    assert body["shared_tickets"] is False
    assert body["shared_comments"] is False


def test_create_skips_none_optional_fields():
    cmd = CreateOrganizationCmd(name="Acme")
    body = to_payload_create(cmd)["organization"]
    assert body == {"name": "Acme"}
    assert "details" not in body
    assert "notes" not in body
    assert "group_id" not in body
    assert "domain_names" not in body
    assert "tags" not in body


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateOrganizationCmd()) == {"organization": {}}


def test_update_with_name_only():
    body = to_payload_update(UpdateOrganizationCmd(name="Acme v2"))["organization"]
    assert body == {"name": "Acme v2"}


def test_update_includes_all_fields():
    cmd = UpdateOrganizationCmd(
        name="Acme",
        domain_names=["acme.com"],
        details="details",
        notes="notes",
        group_id=42,
        shared_tickets=True,
        shared_comments=False,
        tags=["vip"],
        organization_fields={"k": "v"},
        external_id="ext-2",
    )
    body = to_payload_update(cmd)["organization"]
    assert body == {
        "name": "Acme",
        "domain_names": ["acme.com"],
        "details": "details",
        "notes": "notes",
        "group_id": 42,
        "shared_tickets": True,
        "shared_comments": False,
        "tags": ["vip"],
        "organization_fields": {"k": "v"},
        "external_id": "ext-2",
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(
        UpdateOrganizationCmd(shared_tickets=False, shared_comments=False)
    )["organization"]
    assert body["shared_tickets"] is False
    assert body["shared_comments"] is False


def test_update_converts_iterables_to_lists():
    body = to_payload_update(
        UpdateOrganizationCmd(
            domain_names=iter(["a.com"]),
            tags=iter(["t1"]),
        )
    )["organization"]
    assert body["domain_names"] == ["a.com"]
    assert body["tags"] == ["t1"]
