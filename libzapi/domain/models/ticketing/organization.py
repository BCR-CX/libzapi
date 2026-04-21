from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Any

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Organization:
    id: int
    url: str
    name: str
    shared_tickets: bool
    shared_comments: bool
    created_at: datetime
    updated_at: datetime
    domain_names: List[str]
    details: Optional[str]
    notes: Optional[str]
    tags: list[str]
    organization_fields: dict[str, Any]
    group_id: Optional[int] = None
    external_id: Optional[str] = None

    @property
    def logical_key(self) -> LogicalKey:
        base = self.name.lower().replace(" ", "_")
        return LogicalKey("organization", base)


@dataclass(frozen=True, slots=True)
class OrganizationRelated:
    tickets_count: int = 0
    users_count: int = 0
