from __future__ import annotations

from libzapi.application.commands.ticketing.dynamic_content_cmds import (
    CreateDynamicContentItemCmd,
    CreateDynamicContentVariantCmd,
    DynamicContentVariantInputCmd,
    UpdateDynamicContentItemCmd,
    UpdateDynamicContentVariantCmd,
)


def _variant_input_to_payload(variant: DynamicContentVariantInputCmd) -> dict:
    payload: dict = {
        "content": variant.content,
        "locale_id": int(variant.locale_id),
    }
    if variant.default is not None:
        payload["default"] = variant.default
    if variant.active is not None:
        payload["active"] = variant.active
    return payload


def to_payload_create_item(cmd: CreateDynamicContentItemCmd) -> dict:
    return {
        "item": {
            "name": cmd.name,
            "default_locale_id": int(cmd.default_locale_id),
            "variants": [_variant_input_to_payload(v) for v in cmd.variants],
        }
    }


def to_payload_update_item(cmd: UpdateDynamicContentItemCmd) -> dict:
    inner: dict = {}
    if cmd.name is not None:
        inner["name"] = cmd.name
    return {"item": inner}


def to_payload_create_variant(cmd: CreateDynamicContentVariantCmd) -> dict:
    inner: dict = {
        "content": cmd.content,
        "locale_id": int(cmd.locale_id),
    }
    if cmd.default is not None:
        inner["default"] = cmd.default
    if cmd.active is not None:
        inner["active"] = cmd.active
    return {"variant": inner}


def to_payload_update_variant(cmd: UpdateDynamicContentVariantCmd) -> dict:
    inner: dict = {}
    if cmd.content is not None:
        inner["content"] = cmd.content
    if cmd.locale_id is not None:
        inner["locale_id"] = int(cmd.locale_id)
    if cmd.default is not None:
        inner["default"] = cmd.default
    if cmd.active is not None:
        inner["active"] = cmd.active
    return {"variant": inner}
