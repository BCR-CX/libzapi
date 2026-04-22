from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class OrganizationMembership:
    id: int
    user_id: int
    organization_id: int
    default: bool
    created_at: datetime
    updated_at: datetime
    url: Optional[str] = None
    organization_name: Optional[str] = None
    view_tickets: Optional[bool] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey(
            "organization_membership",
            f"u{self.user_id}_o{self.organization_id}",
        )
