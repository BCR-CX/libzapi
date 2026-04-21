from __future__ import annotations

from libzapi.application.commands.ticketing.user_cmds import CreateUserCmd, UpdateUserCmd


_OPTIONAL_FIELDS = (
    "email",
    "role",
    "phone",
    "alias",
    "external_id",
    "organization_id",
    "custom_role_id",
    "default_group_id",
    "details",
    "notes",
    "locale_id",
    "time_zone",
    "verified",
    "active",
    "moderator",
    "only_private_comments",
    "restricted_agent",
    "suspended",
    "ticket_restriction",
    "user_fields",
)


def to_payload_create(cmd: CreateUserCmd) -> dict:
    body: dict = {"name": cmd.name}
    for field in _OPTIONAL_FIELDS:
        value = getattr(cmd, field)
        if value is not None:
            body[field] = value
    if cmd.tags is not None:
        body["tags"] = list(cmd.tags)
    return {"user": body}


def to_payload_update(cmd: UpdateUserCmd) -> dict:
    body: dict = {}
    if cmd.name is not None:
        body["name"] = cmd.name
    for field in _OPTIONAL_FIELDS:
        value = getattr(cmd, field)
        if value is not None:
            body[field] = value
    if cmd.tags is not None:
        body["tags"] = list(cmd.tags)
    return {"user": body}
