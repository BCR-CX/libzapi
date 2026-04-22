from libzapi.application.commands.ticketing.organization_field_cmds import (
    CreateOrganizationFieldCmd,
    OrganizationFieldOptionCmd,
    UpdateOrganizationFieldCmd,
)
from libzapi.infrastructure.mappers.ticketing.organization_field_mapper import (
    option_to_payload,
    to_payload_create,
    to_payload_update,
)


def test_create_minimal():
    payload = to_payload_create(
        CreateOrganizationFieldCmd(key="tier", type="text", title="Tier")
    )
    assert payload == {
        "organization_field": {"key": "tier", "type": "text", "title": "Tier"}
    }


def test_create_with_optionals():
    payload = to_payload_create(
        CreateOrganizationFieldCmd(
            key="priority",
            type="dropdown",
            title="Priority",
            description="d",
            active=True,
            position=5,
            regexp_for_validation="^a$",
            tag="p",
            custom_field_options=[{"name": "A", "value": "a"}],
        )
    )
    assert payload == {
        "organization_field": {
            "key": "priority",
            "type": "dropdown",
            "title": "Priority",
            "description": "d",
            "active": True,
            "position": 5,
            "regexp_for_validation": "^a$",
            "tag": "p",
            "custom_field_options": [{"name": "A", "value": "a"}],
        }
    }


def test_create_preserves_false_active():
    payload = to_payload_create(
        CreateOrganizationFieldCmd(
            key="k", type="text", title="t", active=False
        )
    )
    assert payload["organization_field"]["active"] is False


def test_update_empty():
    assert to_payload_update(UpdateOrganizationFieldCmd()) == {
        "organization_field": {}
    }


def test_update_with_fields():
    payload = to_payload_update(
        UpdateOrganizationFieldCmd(key="k", title="t", position=2, active=False)
    )
    assert payload == {
        "organization_field": {
            "key": "k",
            "title": "t",
            "position": 2,
            "active": False,
        }
    }


def test_option_payload_minimal():
    assert option_to_payload(OrganizationFieldOptionCmd(name="A", value="a")) == {
        "custom_field_option": {"name": "A", "value": "a"}
    }


def test_option_payload_with_id():
    assert option_to_payload(
        OrganizationFieldOptionCmd(name="A", value="a", id=7)
    ) == {"custom_field_option": {"name": "A", "value": "a", "id": 7}}
