from __future__ import annotations

from libzapi.application.commands.ticketing.organization_cmds import (
    CreateOrganizationCmd,
    UpdateOrganizationCmd,
)


_OPTIONAL_FIELDS = (
    "details",
    "notes",
    "group_id",
    "shared_tickets",
    "shared_comments",
    "organization_fields",
    "external_id",
)


def to_payload_create(cmd: CreateOrganizationCmd) -> dict:
    body: dict = {"name": cmd.name}
    for field in _OPTIONAL_FIELDS:
        value = getattr(cmd, field)
        if value is not None:
            body[field] = value
    if cmd.domain_names is not None:
        body["domain_names"] = list(cmd.domain_names)
    if cmd.tags is not None:
        body["tags"] = list(cmd.tags)
    return {"organization": body}


def to_payload_update(cmd: UpdateOrganizationCmd) -> dict:
    body: dict = {}
    if cmd.name is not None:
        body["name"] = cmd.name
    for field in _OPTIONAL_FIELDS:
        value = getattr(cmd, field)
        if value is not None:
            body[field] = value
    if cmd.domain_names is not None:
        body["domain_names"] = list(cmd.domain_names)
    if cmd.tags is not None:
        body["tags"] = list(cmd.tags)
    return {"organization": body}
