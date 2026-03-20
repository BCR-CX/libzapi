from dataclasses import dataclass
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AssetField:
    id: int
    key: str
    title: str
    type: str = ""
    description: str | None = None
    active: bool = True
    system: bool = False
    position: int = 0
    regexp_for_validation: str | None = None
    raw_title: str | None = None
    raw_description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    url: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("asset_field", self.key)
