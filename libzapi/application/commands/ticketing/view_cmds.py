from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateViewCmd:
    title: str
    all: Iterable[dict[str, Any]] | None = None
    any: Iterable[dict[str, Any]] | None = None
    description: str | None = None
    active: bool | None = None
    position: int | None = None
    output: dict[str, Any] | None = None
    restriction: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class UpdateViewCmd:
    title: str | None = None
    all: Iterable[dict[str, Any]] | None = None
    any: Iterable[dict[str, Any]] | None = None
    description: str | None = None
    active: bool | None = None
    position: int | None = None
    output: dict[str, Any] | None = None
    restriction: dict[str, Any] | None = None


ViewCmd: TypeAlias = CreateViewCmd | UpdateViewCmd
