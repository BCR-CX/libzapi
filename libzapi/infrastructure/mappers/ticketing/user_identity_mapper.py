from __future__ import annotations

from libzapi.application.commands.ticketing.user_identity_cmds import (
    CreateUserIdentityCmd,
    UpdateUserIdentityCmd,
)


def to_payload_create(cmd: CreateUserIdentityCmd) -> dict:
    body: dict = {"type": cmd.type, "value": cmd.value}
    if cmd.verified is not None:
        body["verified"] = cmd.verified
    if cmd.primary is not None:
        body["primary"] = cmd.primary
    return {"identity": body}


def to_payload_update(cmd: UpdateUserIdentityCmd) -> dict:
    body: dict = {}
    if cmd.value is not None:
        body["value"] = cmd.value
    if cmd.verified is not None:
        body["verified"] = cmd.verified
    return {"identity": body}
