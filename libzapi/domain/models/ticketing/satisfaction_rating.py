from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class SatisfactionRating:
    id: int
    score: str
    ticket_id: int
    created_at: datetime
    updated_at: datetime
    url: Optional[str] = None
    assignee_id: Optional[int] = None
    group_id: Optional[int] = None
    requester_id: Optional[int] = None
    comment: Optional[str] = None
    reason: Optional[str] = None
    reason_id: Optional[int] = None
    reason_code: Optional[int] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("satisfaction_rating", f"rating_id_{self.id}")


@dataclass(frozen=True, slots=True)
class SatisfactionReason:
    id: int
    reason_code: int
    raw_reason: dict
    reason: dict
    value: str
    created_at: datetime
    updated_at: datetime
    url: Optional[str] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("satisfaction_reason", f"reason_id_{self.id}")
