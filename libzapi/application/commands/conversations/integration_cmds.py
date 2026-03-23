from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CreateIntegrationCmd:
    type: str
    displayName: str = ""
    extra: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class UpdateIntegrationCmd:
    displayName: str | None = None
    extra: dict | None = None
