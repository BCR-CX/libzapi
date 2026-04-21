from __future__ import annotations

from libzapi.application.commands.ticketing.view_cmds import (
    CreateViewCmd,
    UpdateViewCmd,
)


def to_payload_create(cmd: CreateViewCmd) -> dict:
    body: dict = {"title": cmd.title}
    if cmd.all is not None:
        body["all"] = list(cmd.all)
    if cmd.any is not None:
        body["any"] = list(cmd.any)
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.position is not None:
        body["position"] = cmd.position
    if cmd.output is not None:
        body["output"] = cmd.output
    if cmd.restriction is not None:
        body["restriction"] = cmd.restriction
    return {"view": body}


def to_payload_update(cmd: UpdateViewCmd) -> dict:
    body: dict = {}
    if cmd.title is not None:
        body["title"] = cmd.title
    if cmd.all is not None:
        body["all"] = list(cmd.all)
    if cmd.any is not None:
        body["any"] = list(cmd.any)
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.active is not None:
        body["active"] = cmd.active
    if cmd.position is not None:
        body["position"] = cmd.position
    if cmd.output is not None:
        body["output"] = cmd.output
    if cmd.restriction is not None:
        body["restriction"] = cmd.restriction
    return {"view": body}
