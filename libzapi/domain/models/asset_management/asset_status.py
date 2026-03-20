from dataclasses import dataclass
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AssetStatus:
    id: str
    name: str
    external_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    url: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("asset_status", self.name.lower().replace(" ", "_"))
