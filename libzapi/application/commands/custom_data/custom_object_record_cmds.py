from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CreateCustomObjectRecordCmd:
    name: str
    custom_object_fields: dict[str, str] = field(default_factory=dict)
    external_id: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateCustomObjectRecordCmd:
    custom_object_fields: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class BulkJobCmd:
    action: str
    items: list[dict] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class FilteredSearchCmd:
    filter: dict = field(default_factory=dict)
