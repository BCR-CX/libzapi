from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CreateObjectTriggerCmd:
    title: str
    conditions: dict
    actions: list[dict]
    active: bool = True
    description: str = ""


@dataclass(frozen=True, slots=True)
class UpdateObjectTriggerCmd:
    title: str | None = None
    conditions: dict | None = None
    actions: list[dict] | None = None
    active: bool | None = None
    description: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateManyTriggersCmd:
    triggers: list[dict] = field(default_factory=list)
