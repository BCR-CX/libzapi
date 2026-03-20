from dataclasses import dataclass
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Asset:
    id: str
    name: str
    asset_type_id: str
    status_id: str
    url: str = ""
    asset_tag: str | None = None
    location_id: str | None = None
    user_id: int | None = None
    organization_id: int | None = None
    serial_number: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    vendor: str | None = None
    purchase_cost: float | None = None
    purchase_date: str | None = None
    warranty_expiration: str | None = None
    external_id: str | None = None
    notes: str | None = None
    custom_field_values: dict | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("asset", self.id)
