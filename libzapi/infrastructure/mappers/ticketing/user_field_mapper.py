from __future__ import annotations

from libzapi.application.commands.ticketing.user_field_cmds import (
    CreateUserFieldCmd,
    UpdateUserFieldCmd,
    UserFieldOptionCmd,
)


def _add_optionals(body: dict, cmd: CreateUserFieldCmd | UpdateUserFieldCmd) -> None:
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.position is not None:
        body["position"] = cmd.position
    if cmd.regexp_for_validation is not None:
        body["regexp_for_validation"] = cmd.regexp_for_validation
    if cmd.tag is not None:
        body["tag"] = cmd.tag
    if cmd.relationship_target_type is not None:
        body["relationship_target_type"] = cmd.relationship_target_type
    if cmd.relationship_filter is not None:
        body["relationship_filter"] = cmd.relationship_filter
    if cmd.custom_field_options is not None:
        body["custom_field_options"] = list(cmd.custom_field_options)


def to_payload_create(cmd: CreateUserFieldCmd) -> dict:
    body: dict = {"key": cmd.key, "type": cmd.type, "title": cmd.title}
    _add_optionals(body, cmd)
    return {"user_field": body}


def to_payload_update(cmd: UpdateUserFieldCmd) -> dict:
    body: dict = {}
    if cmd.key is not None:
        body["key"] = cmd.key
    if cmd.title is not None:
        body["title"] = cmd.title
    _add_optionals(body, cmd)
    return {"user_field": body}


def option_to_payload(cmd: UserFieldOptionCmd) -> dict:
    body: dict = {"name": cmd.name, "value": cmd.value}
    if cmd.id is not None:
        body["id"] = cmd.id
    return {"custom_field_option": body}
