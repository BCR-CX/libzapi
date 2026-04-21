from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateBrandCmd:
    name: str
    subdomain: str
    active: bool | None = None
    host_mapping: str | None = None
    signature_template: str | None = None
    ticket_form_ids: Iterable[int] | None = None
    brand_url: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateBrandCmd:
    name: str | None = None
    subdomain: str | None = None
    active: bool | None = None
    host_mapping: str | None = None
    signature_template: str | None = None
    ticket_form_ids: Iterable[int] | None = None
    brand_url: str | None = None
    default: bool | None = None


BrandCmd: TypeAlias = CreateBrandCmd | UpdateBrandCmd
