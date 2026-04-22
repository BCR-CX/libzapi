from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Locale:
    id: int
    locale: str
    name: str
    url: Optional[str] = None
    native_name: Optional[str] = None
    presentation_name: Optional[str] = None
    rtl: bool = False
    default: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("locale", self.locale.lower().replace("-", "_"))
