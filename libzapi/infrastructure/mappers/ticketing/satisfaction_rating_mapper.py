from __future__ import annotations

from libzapi.application.commands.ticketing.satisfaction_rating_cmds import (
    CreateSatisfactionRatingCmd,
)


def to_payload_create(cmd: CreateSatisfactionRatingCmd) -> dict:
    body: dict = {"score": cmd.score}
    if cmd.comment is not None:
        body["comment"] = cmd.comment
    if cmd.reason_id is not None:
        body["reason_id"] = int(cmd.reason_id)
    return {"satisfaction_rating": body}
