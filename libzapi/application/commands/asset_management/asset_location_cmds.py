from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateAssetLocationCmd:
    name: str
    external_id: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateAssetLocationCmd:
    name: str | None = None
    external_id: str | None = None
