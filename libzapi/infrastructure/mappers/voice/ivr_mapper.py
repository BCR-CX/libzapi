from libzapi.application.commands.voice.ivr_cmds import (
    CreateIvrCmd,
    UpdateIvrCmd,
    CreateIvrMenuCmd,
    UpdateIvrMenuCmd,
    CreateIvrRouteCmd,
    UpdateIvrRouteCmd,
)


def to_payload_create_ivr(cmd: CreateIvrCmd) -> dict:
    payload: dict = {"name": cmd.name}
    if cmd.phone_number_ids:
        payload["phone_number_ids"] = cmd.phone_number_ids
    return {"ivr": payload}


def to_payload_update_ivr(cmd: UpdateIvrCmd) -> dict:
    fields = ("name", "phone_number_ids")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"ivr": patch}


def to_payload_create_menu(cmd: CreateIvrMenuCmd) -> dict:
    payload: dict = {"name": cmd.name}
    if cmd.default:
        payload["default"] = cmd.default
    if cmd.greeting_id is not None:
        payload["greeting_id"] = cmd.greeting_id
    return {"menu": payload}


def to_payload_update_menu(cmd: UpdateIvrMenuCmd) -> dict:
    fields = ("name", "default", "greeting_id")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"menu": patch}


def to_payload_create_route(cmd: CreateIvrRouteCmd) -> dict:
    payload: dict = {"action": cmd.action, "keypress": cmd.keypress}
    if cmd.options:
        payload["options"] = cmd.options
    if cmd.tags:
        payload["tags"] = cmd.tags
    return {"route": payload}


def to_payload_update_route(cmd: UpdateIvrRouteCmd) -> dict:
    fields = ("action", "keypress", "options", "tags")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"route": patch}
