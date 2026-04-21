from __future__ import annotations

from libzapi.application.commands.ticketing.sla_policy_cmds import (
    CreateSlaPolicyCmd,
    UpdateSlaPolicyCmd,
)


def to_payload_create(cmd: CreateSlaPolicyCmd) -> dict:
    body: dict = {
        "title": cmd.title,
        "filter": cmd.filter,
        "policy_metrics": list(cmd.policy_metrics),
    }
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.position is not None:
        body["position"] = cmd.position
    return {"sla_policy": body}


def to_payload_update(cmd: UpdateSlaPolicyCmd) -> dict:
    body: dict = {}
    if cmd.title is not None:
        body["title"] = cmd.title
    if cmd.filter is not None:
        body["filter"] = cmd.filter
    if cmd.policy_metrics is not None:
        body["policy_metrics"] = list(cmd.policy_metrics)
    if cmd.description is not None:
        body["description"] = cmd.description
    if cmd.position is not None:
        body["position"] = cmd.position
    return {"sla_policy": body}
