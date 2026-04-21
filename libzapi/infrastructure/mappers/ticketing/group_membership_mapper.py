from __future__ import annotations

from libzapi.application.commands.ticketing.group_membership_cmds import (
    CreateGroupMembershipCmd,
)


def to_payload_create(cmd: CreateGroupMembershipCmd) -> dict:
    body: dict = {"user_id": int(cmd.user_id), "group_id": int(cmd.group_id)}
    if cmd.default is not None:
        body["default"] = cmd.default
    return {"group_membership": body}
