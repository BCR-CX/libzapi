from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True, slots=True)
class DynamicContentVariantInputCmd:
    content: str
    locale_id: int
    default: Optional[bool] = None
    active: Optional[bool] = None


@dataclass(frozen=True, slots=True)
class CreateDynamicContentItemCmd:
    name: str
    default_locale_id: int
    variants: List[DynamicContentVariantInputCmd] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class UpdateDynamicContentItemCmd:
    name: Optional[str] = None


@dataclass(frozen=True, slots=True)
class CreateDynamicContentVariantCmd:
    content: str
    locale_id: int
    default: Optional[bool] = None
    active: Optional[bool] = None


@dataclass(frozen=True, slots=True)
class UpdateDynamicContentVariantCmd:
    content: Optional[str] = None
    locale_id: Optional[int] = None
    default: Optional[bool] = None
    active: Optional[bool] = None
