from __future__ import annotations

from libzapi.application.commands.ticketing.support_address_cmds import (
    CreateSupportAddressCmd,
    UpdateSupportAddressCmd,
)


_OPTIONAL_FIELDS = ("name", "brand_id", "default")


def _add_optionals(body: dict, cmd) -> None:
    for field in _OPTIONAL_FIELDS:
        value = getattr(cmd, field)
        if value is not None:
            body[field] = value


def to_payload_create(cmd: CreateSupportAddressCmd) -> dict:
    body: dict = {"email": cmd.email}
    _add_optionals(body, cmd)
    return {"recipient_address": body}


def to_payload_update(cmd: UpdateSupportAddressCmd) -> dict:
    body: dict = {}
    _add_optionals(body, cmd)
    return {"recipient_address": body}
