from __future__ import annotations

from libzapi.application.commands.ticketing.organization_membership_cmds import (
    CreateOrganizationMembershipCmd,
)


def to_payload_create(cmd: CreateOrganizationMembershipCmd) -> dict:
    body: dict = {
        "user_id": int(cmd.user_id),
        "organization_id": int(cmd.organization_id),
    }
    if cmd.default is not None:
        body["default"] = cmd.default
    if cmd.view_tickets is not None:
        body["view_tickets"] = cmd.view_tickets
    return {"organization_membership": body}
