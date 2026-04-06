from dataclasses import dataclass
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class RecordAttachment:
    id: str
    file_name: str = ""
    content_url: str = ""
    content_type: str = ""
    size: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
    malware_access_override: bool = False

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("record_attachment", self.id)
