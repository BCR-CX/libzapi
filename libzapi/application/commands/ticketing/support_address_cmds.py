from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class CreateSupportAddressCmd:
    email: str
    name: str | None = None
    brand_id: int | None = None
    default: bool | None = None


@dataclass(frozen=True, slots=True)
class UpdateSupportAddressCmd:
    name: str | None = None
    brand_id: int | None = None
    default: bool | None = None


SupportAddressCmd: TypeAlias = CreateSupportAddressCmd | UpdateSupportAddressCmd
