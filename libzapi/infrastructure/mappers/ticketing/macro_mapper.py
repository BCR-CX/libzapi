from __future__ import annotations

from libzapi.application.commands.ticketing.macro_cmds import (
    CreateMacroCmd,
    UpdateMacroCmd,
)


def to_payload_create(cmd: CreateMacroCmd) -> dict:
    body: dict = {"title": cmd.title, "actions": list(cmd.actions)}
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.restriction is not None:
        body["restriction"] = cmd.restriction
    return {"macro": body}


def to_payload_update(cmd: UpdateMacroCmd) -> dict:
    body: dict = {}
    if cmd.title is not None:
        body["title"] = cmd.title
    if cmd.actions is not None:
        body["actions"] = list(cmd.actions)
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.restriction is not None:
        body["restriction"] = cmd.restriction
    if cmd.position is not None:
        body["position"] = cmd.position
    return {"macro": body}
