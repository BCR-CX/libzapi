from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class TicketActivity:
    id: int
    verb: str
    title: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int] = None
    actor_id: Optional[int] = None
    url: Optional[str] = None
    actor: Optional[dict] = None
    user: Optional[dict] = None
    object: Optional[dict] = None
    target: Optional[dict] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("ticket_activity", f"activity_id_{self.id}")
