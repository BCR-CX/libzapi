from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateOrganizationFieldCmd:
    key: str
    type: str
    title: str
    description: str | None = None
    active: bool | None = None
    position: int | None = None
    regexp_for_validation: str | None = None
    tag: str | None = None
    custom_field_options: Iterable[dict[str, Any]] | None = None


@dataclass(frozen=True, slots=True)
class UpdateOrganizationFieldCmd:
    key: str | None = None
    title: str | None = None
    description: str | None = None
    active: bool | None = None
    position: int | None = None
    regexp_for_validation: str | None = None
    tag: str | None = None
    custom_field_options: Iterable[dict[str, Any]] | None = None


@dataclass(frozen=True, slots=True)
class OrganizationFieldOptionCmd:
    name: str
    value: str
    id: int | None = None


OrganizationFieldCmd: TypeAlias = (
    CreateOrganizationFieldCmd | UpdateOrganizationFieldCmd
)
