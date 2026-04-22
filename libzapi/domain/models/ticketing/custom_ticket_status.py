from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class CustomTicketStatus:
    id: int
    status_category: str
    agent_label: str
    end_user_label: str
    created_at: datetime
    updated_at: datetime
    active: bool = True
    default: bool = False
    description: Optional[str] = None
    end_user_description: Optional[str] = None
    raw_agent_label: Optional[str] = None
    raw_description: Optional[str] = None
    raw_end_user_description: Optional[str] = None
    raw_end_user_label: Optional[str] = None
    url: Optional[str] = None
    excluded_from_forms: List[int] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("custom_ticket_status", f"status_id_{self.id}")
