from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class CreateUserIdentityCmd:
    type: str
    value: str
    verified: bool | None = None
    primary: bool | None = None


@dataclass(frozen=True, slots=True)
class UpdateUserIdentityCmd:
    value: str | None = None
    verified: bool | None = None


UserIdentityCmd: TypeAlias = CreateUserIdentityCmd | UpdateUserIdentityCmd
