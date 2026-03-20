from dataclasses import dataclass
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AssetType:
    id: str
    name: str
    parent_id: str = ""
    description: str | None = None
    external_id: str | None = None
    field_keys: list[str] | None = None
    hierarchy_depth: int = 1
    is_standard: bool = False
    created_at: datetime | None = None
    created_by_user_id: int | None = None
    updated_at: datetime | None = None
    updated_by_user_id: int | None = None
    url: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        base = self.name.lower().replace(" ", "_")
        return LogicalKey("asset_type", base)
