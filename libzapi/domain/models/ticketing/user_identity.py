from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class UserIdentity:
    id: int
    user_id: int
    type: str
    value: str
    verified: bool
    primary: bool
    created_at: datetime
    updated_at: datetime
    url: Optional[str] = None
    undeliverable_count: Optional[int] = None
    deliverable_state: Optional[str] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey(
            "user_identity", f"u{self.user_id}_id{self.id}"
        )
