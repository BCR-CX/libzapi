from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateOrganizationCmd:
    name: str
    domain_names: Iterable[str] | None = None
    details: str | None = None
    notes: str | None = None
    group_id: int | None = None
    shared_tickets: bool | None = None
    shared_comments: bool | None = None
    tags: Iterable[str] | None = None
    organization_fields: dict[str, Any] | None = None
    external_id: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateOrganizationCmd:
    name: str | None = None
    domain_names: Iterable[str] | None = None
    details: str | None = None
    notes: str | None = None
    group_id: int | None = None
    shared_tickets: bool | None = None
    shared_comments: bool | None = None
    tags: Iterable[str] | None = None
    organization_fields: dict[str, Any] | None = None
    external_id: str | None = None


OrganizationCmd: TypeAlias = CreateOrganizationCmd | UpdateOrganizationCmd
