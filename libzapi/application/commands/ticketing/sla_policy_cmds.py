from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateSlaPolicyCmd:
    title: str
    filter: dict[str, Any]
    policy_metrics: Iterable[dict[str, Any]]
    description: str | None = None
    position: int | None = None


@dataclass(frozen=True, slots=True)
class UpdateSlaPolicyCmd:
    title: str | None = None
    filter: dict[str, Any] | None = None
    policy_metrics: Iterable[dict[str, Any]] | None = None
    description: str | None = None
    position: int | None = None


SlaPolicyCmd: TypeAlias = CreateSlaPolicyCmd | UpdateSlaPolicyCmd
