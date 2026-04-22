from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class TicketSkip:
    id: int
    user_id: int
    ticket_id: int
    reason: str
    created_at: datetime
    updated_at: datetime
    ticket: Optional[dict] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("ticket_skip", f"skip_id_{self.id}")
