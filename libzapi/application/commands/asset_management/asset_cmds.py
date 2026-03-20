from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateAssetCmd:
    name: str
    asset_type_id: str
    status_id: str
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


@dataclass(frozen=True, slots=True)
class UpdateAssetCmd:
    name: str | None = None
    status_id: str | None = None
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
