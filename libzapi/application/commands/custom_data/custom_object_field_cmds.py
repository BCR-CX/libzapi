from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateCustomObjectFieldCmd:
    type: str
    key: str
    title: str
    description: str = ""
    active: bool = True
    position: int = 0
    regexp_for_validation: str | None = None
    custom_field_options: list[dict] | None = None
    relationship_target_type: str | None = None
    relationship_filter: dict | None = None
    tag: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateCustomObjectFieldCmd:
    title: str | None = None
    description: str | None = None
    active: bool | None = None
    position: int | None = None
    custom_field_options: list[dict] | None = None
