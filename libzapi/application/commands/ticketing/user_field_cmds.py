from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateUserFieldCmd:
    key: str
    type: str
    title: str
    description: str | None = None
    active: bool | None = None
    position: int | None = None
    regexp_for_validation: str | None = None
    tag: str | None = None
    relationship_target_type: str | None = None
    relationship_filter: dict[str, Any] | None = None
    custom_field_options: Iterable[dict[str, Any]] | None = None


@dataclass(frozen=True, slots=True)
class UpdateUserFieldCmd:
    key: str | None = None
    title: str | None = None
    description: str | None = None
    active: bool | None = None
    position: int | None = None
    regexp_for_validation: str | None = None
    tag: str | None = None
    relationship_target_type: str | None = None
    relationship_filter: dict[str, Any] | None = None
    custom_field_options: Iterable[dict[str, Any]] | None = None


@dataclass(frozen=True, slots=True)
class UserFieldOptionCmd:
    name: str
    value: str
    id: int | None = None


UserFieldCmd: TypeAlias = CreateUserFieldCmd | UpdateUserFieldCmd
