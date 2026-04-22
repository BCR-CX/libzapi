from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateSatisfactionRatingCmd:
    score: str
    comment: str | None = None
    reason_id: int | None = None
