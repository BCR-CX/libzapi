from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CreateIvrCmd:
    name: str
    phone_number_ids: list[int] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class UpdateIvrCmd:
    name: str | None = None
    phone_number_ids: list[int] | None = None


@dataclass(frozen=True, slots=True)
class CreateIvrMenuCmd:
    name: str
    default: bool = False
    greeting_id: int | None = None


@dataclass(frozen=True, slots=True)
class UpdateIvrMenuCmd:
    name: str | None = None
    default: bool | None = None
    greeting_id: int | None = None


@dataclass(frozen=True, slots=True)
class CreateIvrRouteCmd:
    action: str
    keypress: str
    options: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class UpdateIvrRouteCmd:
    action: str | None = None
    keypress: str | None = None
    options: dict | None = None
    tags: list[str] | None = None
