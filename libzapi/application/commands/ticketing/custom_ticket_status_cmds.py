from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class CreateCustomTicketStatusCmd:
    status_category: str
    agent_label: str
    end_user_label: str | None = None
    description: str | None = None
    end_user_description: str | None = None
    active: bool | None = None


@dataclass(frozen=True, slots=True)
class UpdateCustomTicketStatusCmd:
    agent_label: str | None = None
    end_user_label: str | None = None
    description: str | None = None
    end_user_description: str | None = None
    active: bool | None = None


CustomTicketStatusCmd: TypeAlias = (
    CreateCustomTicketStatusCmd | UpdateCustomTicketStatusCmd
)
