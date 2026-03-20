from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateAssetTypeCmd:
    name: str
    parent_id: str
    description: str | None = None
    external_id: str | None = None
    field_keys: list[str] | None = None


@dataclass(frozen=True, slots=True)
class UpdateAssetTypeCmd:
    description: str | None = None
    external_id: str | None = None
    field_keys: list[str] | None = None
