from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserCmd:
    externalId: str
    profile: dict | None = None
    metadata: dict | None = None


@dataclass(frozen=True, slots=True)
class UpdateUserCmd:
    profile: dict | None = None
    metadata: dict | None = None
