from __future__ import annotations

from libzapi.application.commands.ticketing.request_cmds import (
    CreateRequestCmd,
    UpdateRequestCmd,
)


def to_payload_create(cmd: CreateRequestCmd) -> dict:
    body: dict = {"subject": cmd.subject, "comment": dict(cmd.comment)}
    if cmd.requester is not None:
        body["requester"] = dict(cmd.requester)
    if cmd.priority is not None:
        body["priority"] = cmd.priority
    if cmd.type is not None:
        body["type"] = cmd.type
    if cmd.custom_fields is not None:
        body["custom_fields"] = [dict(f) for f in cmd.custom_fields]
    if cmd.ticket_form_id is not None:
        body["ticket_form_id"] = cmd.ticket_form_id
    if cmd.recipient is not None:
        body["recipient"] = cmd.recipient
    if cmd.collaborators is not None:
        body["collaborators"] = list(cmd.collaborators)
    if cmd.email_ccs is not None:
        body["email_ccs"] = list(cmd.email_ccs)
    if cmd.due_at is not None:
        body["due_at"] = cmd.due_at
    return {"request": body}


def to_payload_update(cmd: UpdateRequestCmd) -> dict:
    body: dict = {}
    if cmd.comment is not None:
        body["comment"] = dict(cmd.comment)
    if cmd.solved is not None:
        body["solved"] = cmd.solved
    if cmd.additional_collaborators is not None:
        body["additional_collaborators"] = list(cmd.additional_collaborators)
    if cmd.email_ccs is not None:
        body["email_ccs"] = list(cmd.email_ccs)
    return {"request": body}
