from __future__ import annotations

from libzapi.application.commands.ticketing.automation_cmds import (
    CreateAutomationCmd,
    UpdateAutomationCmd,
)


def to_payload_create(cmd: CreateAutomationCmd) -> dict:
    body: dict = {
        "title": cmd.title,
        "actions": list(cmd.actions),
        "conditions": cmd.conditions,
    }
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.position is not None:
        body["position"] = cmd.position
    return {"automation": body}


def to_payload_update(cmd: UpdateAutomationCmd) -> dict:
    body: dict = {}
    if cmd.title is not None:
        body["title"] = cmd.title
    if cmd.actions is not None:
        body["actions"] = list(cmd.actions)
    if cmd.conditions is not None:
        body["conditions"] = cmd.conditions
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.position is not None:
        body["position"] = cmd.position
    return {"automation": body}
