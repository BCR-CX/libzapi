from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateRequestCmd:
    subject: str
    comment: dict[str, Any]
    requester: dict[str, Any] | None = None
    priority: str | None = None
    type: str | None = None
    custom_fields: Iterable[dict[str, Any]] | None = None
    ticket_form_id: int | None = None
    recipient: str | None = None
    collaborators: Iterable[Any] | None = None
    email_ccs: Iterable[Any] | None = None
    due_at: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateRequestCmd:
    comment: dict[str, Any] | None = None
    solved: bool | None = None
    additional_collaborators: Iterable[Any] | None = None
    email_ccs: Iterable[Any] | None = None


RequestCmd: TypeAlias = CreateRequestCmd | UpdateRequestCmd
