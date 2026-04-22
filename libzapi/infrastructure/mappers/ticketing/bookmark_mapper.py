from __future__ import annotations

from libzapi.application.commands.ticketing.bookmark_cmds import CreateBookmarkCmd


def to_payload_create(cmd: CreateBookmarkCmd) -> dict:
    return {"bookmark": {"ticket_id": int(cmd.ticket_id)}}
