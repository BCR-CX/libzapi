from __future__ import annotations

from libzapi.application.commands.ticketing.ticket_field_cmds import (
    CreateTicketFieldCmd,
    TicketFieldOptionCmd,
    UpdateTicketFieldCmd,
)


def _add_optionals(body: dict, cmd: CreateTicketFieldCmd | UpdateTicketFieldCmd) -> None:
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.required is not None:
        body["required"] = cmd.required
    if cmd.collapsed_for_agents is not None:
        body["collapsed_for_agents"] = cmd.collapsed_for_agents
    if cmd.regexp_for_validation is not None:
        body["regexp_for_validation"] = cmd.regexp_for_validation
    if cmd.title_in_portal is not None:
        body["title_in_portal"] = cmd.title_in_portal
    if cmd.visible_in_portal is not None:
        body["visible_in_portal"] = cmd.visible_in_portal
    if cmd.editable_in_portal is not None:
        body["editable_in_portal"] = cmd.editable_in_portal
    if cmd.required_in_portal is not None:
        body["required_in_portal"] = cmd.required_in_portal
    if cmd.agent_can_edit is not None:
        body["agent_can_edit"] = cmd.agent_can_edit
    if cmd.tag is not None:
        body["tag"] = cmd.tag
    if cmd.position is not None:
        body["position"] = cmd.position
    if cmd.custom_field_options is not None:
        body["custom_field_options"] = list(cmd.custom_field_options)
    if cmd.sub_type_id is not None:
        body["sub_type_id"] = cmd.sub_type_id
    if cmd.relationship_target_type is not None:
        body["relationship_target_type"] = cmd.relationship_target_type
    if cmd.relationship_filter is not None:
        body["relationship_filter"] = cmd.relationship_filter
    if cmd.agent_description is not None:
        body["agent_description"] = cmd.agent_description


def to_payload_create(cmd: CreateTicketFieldCmd) -> dict:
    body: dict = {"title": cmd.title, "type": cmd.type}
    _add_optionals(body, cmd)
    return {"ticket_field": body}


def to_payload_update(cmd: UpdateTicketFieldCmd) -> dict:
    body: dict = {}
    if cmd.title is not None:
        body["title"] = cmd.title
    _add_optionals(body, cmd)
    return {"ticket_field": body}


def option_to_payload(cmd: TicketFieldOptionCmd) -> dict:
    body: dict = {"name": cmd.name, "value": cmd.value}
    if cmd.id is not None:
        body["id"] = cmd.id
    return {"custom_field_option": body}
