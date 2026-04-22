from __future__ import annotations

from libzapi.application.commands.ticketing.ticket_skip_cmds import CreateTicketSkipCmd


def to_payload_create(cmd: CreateTicketSkipCmd) -> dict:
    return {"skip": {"reason": cmd.reason}}
