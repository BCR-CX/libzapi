from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CreateConversationCmd:
    type: str = "personal"
    displayName: str = ""
    description: str = ""
    iconUrl: str = ""
    metadata: dict = field(default_factory=dict)
    participants: list[dict] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class UpdateConversationCmd:
    displayName: str | None = None
    description: str | None = None
    iconUrl: str | None = None
    metadata: dict | None = None
