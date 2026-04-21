from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateWorkspaceCmd:
    title: str
    conditions: dict[str, Any]
    description: str | None = None
    activated: bool | None = None
    prefer_workspace_app_order: bool | None = None
    macros: Iterable[int] | None = None
    apps: Iterable[dict[str, Any]] | None = None
    ticket_form_id: int | None = None
    position: int | None = None


@dataclass(frozen=True, slots=True)
class UpdateWorkspaceCmd:
    title: str | None = None
    description: str | None = None
    conditions: dict[str, Any] | None = None
    activated: bool | None = None
    prefer_workspace_app_order: bool | None = None
    macros: Iterable[int] | None = None
    apps: Iterable[dict[str, Any]] | None = None
    ticket_form_id: int | None = None
    position: int | None = None


WorkspaceCmd: TypeAlias = CreateWorkspaceCmd | UpdateWorkspaceCmd
