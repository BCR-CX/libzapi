from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CreateAppCmd:
    displayName: str
    metadata: dict = field(default_factory=dict)
    settings: dict | None = None


@dataclass(frozen=True, slots=True)
class UpdateAppCmd:
    displayName: str | None = None
    metadata: dict | None = None
    settings: dict | None = None
