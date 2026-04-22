from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class DynamicContentVariant:
    id: int
    content: str
    locale_id: int
    default: bool = False
    active: bool = True
    outdated: bool = False
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("dynamic_content_variant", f"variant_id_{self.id}")


@dataclass(frozen=True, slots=True)
class DynamicContentItem:
    id: int
    name: str
    placeholder: str
    default_locale_id: int
    url: Optional[str] = None
    outdated: bool = False
    variants: List[DynamicContentVariant] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("dynamic_content_item", f"item_id_{self.id}")
