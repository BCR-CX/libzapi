from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Attachment:
    mediaUrl: str = ""
    mediaType: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("sunco_attachment", self.mediaUrl)
