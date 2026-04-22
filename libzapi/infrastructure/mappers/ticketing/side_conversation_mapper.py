from __future__ import annotations

from libzapi.application.commands.ticketing.side_conversation_cmds import (
    CreateSideConversationCmd,
    ReplySideConversationCmd,
    SideConversationMessageCmd,
    UpdateSideConversationCmd,
)


def _message_to_payload(msg: SideConversationMessageCmd) -> dict:
    payload: dict = {"body": msg.body}
    if msg.subject is not None:
        payload["subject"] = msg.subject
    if msg.to:
        payload["to"] = list(msg.to)
    if msg.from_ is not None:
        payload["from"] = msg.from_
    if msg.body_html is not None:
        payload["body_html"] = msg.body_html
    if msg.attachment_ids:
        payload["attachment_ids"] = list(msg.attachment_ids)
    return payload


def to_payload_create(cmd: CreateSideConversationCmd) -> dict:
    payload: dict = {"message": _message_to_payload(cmd.message)}
    if cmd.external_ids is not None:
        payload["external_ids"] = cmd.external_ids
    return {"side_conversation": payload}


def to_payload_reply(cmd: ReplySideConversationCmd) -> dict:
    return {"message": _message_to_payload(cmd.message)}


def to_payload_update(cmd: UpdateSideConversationCmd) -> dict:
    inner: dict = {}
    if cmd.state is not None:
        inner["state"] = cmd.state
    return {"side_conversation": inner}
