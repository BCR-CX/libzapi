from dataclasses import dataclass
from typing import List

from libzapi.domain.models.ticketing.attachment import Attachment
from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Upload:
    token: str
    attachment: Attachment
    attachments: List[Attachment]

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("upload", self.token)
