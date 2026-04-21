from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateMacroCmd:
    title: str
    actions: Iterable[dict[str, Any]]
    active: bool | None = None
    description: str | None = None
    restriction: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class UpdateMacroCmd:
    title: str | None = None
    actions: Iterable[dict[str, Any]] | None = None
    active: bool | None = None
    description: str | None = None
    restriction: dict[str, Any] | None = None
    position: int | None = None


MacroCmd: TypeAlias = CreateMacroCmd | UpdateMacroCmd
