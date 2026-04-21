from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateUserCmd:
    name: str
    email: str | None = None
    role: str | None = None
    phone: str | None = None
    alias: str | None = None
    external_id: str | None = None
    organization_id: int | None = None
    custom_role_id: int | None = None
    default_group_id: int | None = None
    details: str | None = None
    notes: str | None = None
    locale_id: int | None = None
    time_zone: str | None = None
    verified: bool | None = None
    active: bool | None = None
    moderator: bool | None = None
    only_private_comments: bool | None = None
    restricted_agent: bool | None = None
    suspended: bool | None = None
    ticket_restriction: str | None = None
    tags: Iterable[str] | None = None
    user_fields: dict | None = None


@dataclass(frozen=True, slots=True)
class UpdateUserCmd:
    name: str | None = None
    email: str | None = None
    role: str | None = None
    phone: str | None = None
    alias: str | None = None
    external_id: str | None = None
    organization_id: int | None = None
    custom_role_id: int | None = None
    default_group_id: int | None = None
    details: str | None = None
    notes: str | None = None
    locale_id: int | None = None
    time_zone: str | None = None
    verified: bool | None = None
    active: bool | None = None
    moderator: bool | None = None
    only_private_comments: bool | None = None
    restricted_agent: bool | None = None
    suspended: bool | None = None
    ticket_restriction: str | None = None
    tags: Iterable[str] | None = None
    user_fields: dict | None = None


UserCmd: TypeAlias = CreateUserCmd | UpdateUserCmd
