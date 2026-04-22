from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Bookmark:
    id: int
    url: Optional[str] = None
    ticket: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("bookmark", f"bookmark_id_{self.id}")
