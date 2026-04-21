from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class GroupMembership:
    id: int
    user_id: int
    group_id: int
    default: bool
    created_at: datetime
    updated_at: datetime
    url: Optional[str] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("group_membership", f"u{self.user_id}_g{self.group_id}")
