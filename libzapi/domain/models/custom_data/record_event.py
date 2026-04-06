from dataclasses import dataclass
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class RecordEventActor:
    user_id: int | None = None


@dataclass(frozen=True, slots=True)
class RecordEvent:
    id: str
    type: str
    source: str = ""
    description: str = ""
    actor: RecordEventActor | None = None
    created_at: datetime | None = None
    received_at: datetime | None = None
    properties: dict | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("record_event", self.id)
