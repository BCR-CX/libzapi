from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateAutomationCmd:
    title: str
    actions: Iterable[dict[str, Any]]
    conditions: dict[str, Any]
    active: bool | None = None
    position: int | None = None


@dataclass(frozen=True, slots=True)
class UpdateAutomationCmd:
    title: str | None = None
    actions: Iterable[dict[str, Any]] | None = None
    conditions: dict[str, Any] | None = None
    active: bool | None = None
    position: int | None = None


AutomationCmd: TypeAlias = CreateAutomationCmd | UpdateAutomationCmd
