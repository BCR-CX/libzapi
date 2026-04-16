from dataclasses import dataclass, field
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class DigitalLine:
    id: int
    nickname: str = ""
    line_id: str = ""
    line_type: str = ""
    brand_id: int | None = None
    recorded: bool = False
    transcription: bool = False
    default_group_id: int | None = None
    group_ids: list[int] = field(default_factory=list)
    greeting_ids: list[int] = field(default_factory=list)
    default_greeting_ids: list[str] = field(default_factory=list)
    schedule_id: int | None = None
    priority: int = 0
    call_recording_consent: str = ""
    outbound_number: str | None = None
    bot_id: int | None = None
    created_at: datetime | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("digital_line", str(self.id))
