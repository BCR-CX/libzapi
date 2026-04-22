from __future__ import annotations

from libzapi.application.commands.ticketing.custom_ticket_status_cmds import (
    CreateCustomTicketStatusCmd,
    UpdateCustomTicketStatusCmd,
)


_OPTIONAL_STRING_FIELDS = (
    "end_user_label",
    "description",
    "end_user_description",
)


def to_payload_create(cmd: CreateCustomTicketStatusCmd) -> dict:
    body: dict = {
        "status_category": cmd.status_category,
        "agent_label": cmd.agent_label,
    }
    for name in _OPTIONAL_STRING_FIELDS:
        value = getattr(cmd, name)
        if value is not None:
            body[name] = value
    if cmd.active is not None:
        body["active"] = cmd.active
    return {"custom_status": body}


def to_payload_update(cmd: UpdateCustomTicketStatusCmd) -> dict:
    body: dict = {}
    if cmd.agent_label is not None:
        body["agent_label"] = cmd.agent_label
    for name in _OPTIONAL_STRING_FIELDS:
        value = getattr(cmd, name)
        if value is not None:
            body[name] = value
    if cmd.active is not None:
        body["active"] = cmd.active
    return {"custom_status": body}
