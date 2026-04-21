from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateTicketTriggerCmd:
    title: str
    actions: Iterable[dict[str, Any]]
    conditions: dict[str, Any] | None = None
    active: bool | None = None
    description: str | None = None
    category_id: str | None = None
    position: int | None = None


@dataclass(frozen=True, slots=True)
class UpdateTicketTriggerCmd:
    title: str | None = None
    actions: Iterable[dict[str, Any]] | None = None
    conditions: dict[str, Any] | None = None
    active: bool | None = None
    description: str | None = None
    category_id: str | None = None
    position: int | None = None


TicketTriggerCmd: TypeAlias = CreateTicketTriggerCmd | UpdateTicketTriggerCmd
