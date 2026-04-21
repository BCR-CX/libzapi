from __future__ import annotations

from libzapi.application.commands.ticketing.brand_cmds import (
    CreateBrandCmd,
    UpdateBrandCmd,
)


_OPTIONAL_FIELDS = (
    "active",
    "host_mapping",
    "signature_template",
    "brand_url",
)


def to_payload_create(cmd: CreateBrandCmd) -> dict:
    body: dict = {"name": cmd.name, "subdomain": cmd.subdomain}
    for field in _OPTIONAL_FIELDS:
        value = getattr(cmd, field)
        if value is not None:
            body[field] = value
    if cmd.ticket_form_ids is not None:
        body["ticket_form_ids"] = list(cmd.ticket_form_ids)
    return {"brand": body}


def to_payload_update(cmd: UpdateBrandCmd) -> dict:
    body: dict = {}
    if cmd.name is not None:
        body["name"] = cmd.name
    if cmd.subdomain is not None:
        body["subdomain"] = cmd.subdomain
    for field in _OPTIONAL_FIELDS:
        value = getattr(cmd, field)
        if value is not None:
            body[field] = value
    if cmd.ticket_form_ids is not None:
        body["ticket_form_ids"] = list(cmd.ticket_form_ids)
    if cmd.default is not None:
        body["default"] = cmd.default
    return {"brand": body}
