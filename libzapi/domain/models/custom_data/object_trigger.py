from dataclasses import dataclass, field
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class ObjectTrigger:
    id: int
    title: str
    active: bool = True
    position: int | None = None
    conditions: dict = field(default_factory=dict)
    actions: list[dict] = field(default_factory=list)
    description: str = ""
    raw_title: str = ""
    default: bool = False
    url: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("object_trigger", str(self.id))
