from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from libzapi.domain.models.ticketing.attachment import Attachment
from libzapi.domain.shared_objects.logical_key import LogicalKey
from libzapi.domain.shared_objects.via import Via


@dataclass(frozen=True, slots=True)
class Comment:
    id: int
    type: str
    author_id: int
    body: str
    html_body: str
    plain_body: str
    public: bool
    created_at: datetime
    via: Optional[Via] = None
    metadata: Optional[dict] = None
    audit_id: Optional[int] = None
    attachments: List[Attachment] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("ticket_comment", f"comment_id_{self.id}")
