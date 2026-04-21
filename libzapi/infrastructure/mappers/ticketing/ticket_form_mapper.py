from __future__ import annotations

from libzapi.application.commands.ticketing.ticket_form_cmds import (
    CreateTicketFormCmd,
    UpdateTicketFormCmd,
)


def _add_optionals(body: dict, cmd: CreateTicketFormCmd | UpdateTicketFormCmd) -> None:
    if cmd.display_name is not None:
        body["display_name"] = cmd.display_name
    if cmd.end_user_visible is not None:
        body["end_user_visible"] = cmd.end_user_visible
    if cmd.position is not None:
        body["position"] = cmd.position
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.default is not None:
        body["default"] = cmd.default
    if cmd.in_all_brands is not None:
        body["in_all_brands"] = cmd.in_all_brands
    if cmd.restricted_brand_ids is not None:
        body["restricted_brand_ids"] = [int(i) for i in cmd.restricted_brand_ids]
    if cmd.end_user_conditions is not None:
        body["end_user_conditions"] = list(cmd.end_user_conditions)
    if cmd.agent_conditions is not None:
        body["agent_conditions"] = list(cmd.agent_conditions)


def to_payload_create(cmd: CreateTicketFormCmd) -> dict:
    body: dict = {
        "name": cmd.name,
        "ticket_field_ids": [int(i) for i in cmd.ticket_field_ids],
    }
    _add_optionals(body, cmd)
    return {"ticket_form": body}


def to_payload_update(cmd: UpdateTicketFormCmd) -> dict:
    body: dict = {}
    if cmd.name is not None:
        body["name"] = cmd.name
    if cmd.ticket_field_ids is not None:
        body["ticket_field_ids"] = [int(i) for i in cmd.ticket_field_ids]
    _add_optionals(body, cmd)
    return {"ticket_form": body}
