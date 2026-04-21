from __future__ import annotations

from libzapi.application.commands.ticketing.workspace_cmds import (
    CreateWorkspaceCmd,
    UpdateWorkspaceCmd,
)


def _add_optionals(body: dict, cmd: CreateWorkspaceCmd | UpdateWorkspaceCmd) -> None:
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.activated is not None:
        body["activated"] = cmd.activated
    if cmd.prefer_workspace_app_order is not None:
        body["prefer_workspace_app_order"] = cmd.prefer_workspace_app_order
    if cmd.macros is not None:
        body["macros"] = [int(i) for i in cmd.macros]
    if cmd.apps is not None:
        body["apps"] = list(cmd.apps)
    if cmd.ticket_form_id is not None:
        body["ticket_form_id"] = int(cmd.ticket_form_id)
    if cmd.position is not None:
        body["position"] = cmd.position


def to_payload_create(cmd: CreateWorkspaceCmd) -> dict:
    body: dict = {"title": cmd.title, "conditions": cmd.conditions}
    _add_optionals(body, cmd)
    return {"workspace": body}


def to_payload_update(cmd: UpdateWorkspaceCmd) -> dict:
    body: dict = {}
    if cmd.title is not None:
        body["title"] = cmd.title
    if cmd.conditions is not None:
        body["conditions"] = cmd.conditions
    _add_optionals(body, cmd)
    return {"workspace": body}
