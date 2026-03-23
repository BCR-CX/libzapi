from __future__ import annotations

from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Participant:
    id: str
    userId: str = ""
    userExternalId: str = ""
    unreadCount: int = 0
    lastRead: str = ""
    clientAssociations: list[dict] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("participant", self.id)
