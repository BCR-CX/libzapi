from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateTicketFormCmd:
    name: str
    ticket_field_ids: Iterable[int]
    display_name: str | None = None
    end_user_visible: bool | None = None
    position: int | None = None
    active: bool | None = None
    default: bool | None = None
    in_all_brands: bool | None = None
    restricted_brand_ids: Iterable[int] | None = None
    end_user_conditions: Iterable[dict[str, Any]] | None = None
    agent_conditions: Iterable[dict[str, Any]] | None = None


@dataclass(frozen=True, slots=True)
class UpdateTicketFormCmd:
    name: str | None = None
    ticket_field_ids: Iterable[int] | None = None
    display_name: str | None = None
    end_user_visible: bool | None = None
    position: int | None = None
    active: bool | None = None
    default: bool | None = None
    in_all_brands: bool | None = None
    restricted_brand_ids: Iterable[int] | None = None
    end_user_conditions: Iterable[dict[str, Any]] | None = None
    agent_conditions: Iterable[dict[str, Any]] | None = None


TicketFormCmd: TypeAlias = CreateTicketFormCmd | UpdateTicketFormCmd
