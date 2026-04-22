from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class SideConversation:
    id: str
    ticket_id: int
    url: Optional[str] = None
    subject: Optional[str] = None
    preview_text: Optional[str] = None
    state: Optional[str] = None
    participants: List[dict] = field(default_factory=list)
    message_added_at: Optional[datetime] = None
    state_updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    external_ids: Optional[dict] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("side_conversation", f"side_conversation_id_{self.id}")
