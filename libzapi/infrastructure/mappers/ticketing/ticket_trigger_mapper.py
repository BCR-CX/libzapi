from __future__ import annotations

from libzapi.application.commands.ticketing.ticket_trigger_cmds import (
    CreateTicketTriggerCmd,
    UpdateTicketTriggerCmd,
)


def to_payload_create(cmd: CreateTicketTriggerCmd) -> dict:
    body: dict = {"title": cmd.title, "actions": list(cmd.actions)}
    if cmd.conditions is not None:
        body["conditions"] = cmd.conditions
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.category_id is not None:
        body["category_id"] = cmd.category_id
    if cmd.position is not None:
        body["position"] = cmd.position
    return {"trigger": body}


def to_payload_update(cmd: UpdateTicketTriggerCmd) -> dict:
    body: dict = {}
    if cmd.title is not None:
        body["title"] = cmd.title
    if cmd.actions is not None:
        body["actions"] = list(cmd.actions)
    if cmd.conditions is not None:
        body["conditions"] = cmd.conditions
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.category_id is not None:
        body["category_id"] = cmd.category_id
    if cmd.position is not None:
        body["position"] = cmd.position
    return {"trigger": body}
