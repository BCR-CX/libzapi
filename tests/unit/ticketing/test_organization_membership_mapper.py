from libzapi.application.commands.ticketing.organization_membership_cmds import (
    CreateOrganizationMembershipCmd,
)
from libzapi.infrastructure.mappers.ticketing.organization_membership_mapper import (
    to_payload_create,
)


def test_minimal_payload():
    cmd = CreateOrganizationMembershipCmd(user_id=3, organization_id=4)
    assert to_payload_create(cmd) == {
        "organization_membership": {"user_id": 3, "organization_id": 4}
    }


def test_default_included():
    cmd = CreateOrganizationMembershipCmd(
        user_id=3, organization_id=4, default=True
    )
    assert to_payload_create(cmd) == {
        "organization_membership": {
            "user_id": 3,
            "organization_id": 4,
            "default": True,
        }
    }


def test_default_false_preserved():
    cmd = CreateOrganizationMembershipCmd(
        user_id=3, organization_id=4, default=False
    )
    assert to_payload_create(cmd)["organization_membership"]["default"] is False


def test_view_tickets_included():
    cmd = CreateOrganizationMembershipCmd(
        user_id=3, organization_id=4, view_tickets=True
    )
    assert (
        to_payload_create(cmd)["organization_membership"]["view_tickets"]
        is True
    )


def test_view_tickets_false_preserved():
    cmd = CreateOrganizationMembershipCmd(
        user_id=3, organization_id=4, view_tickets=False
    )
    assert (
        to_payload_create(cmd)["organization_membership"]["view_tickets"]
        is False
    )
