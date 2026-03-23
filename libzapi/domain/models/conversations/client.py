from __future__ import annotations

from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Client:
    id: str
    type: str = ""
    status: str = ""
    integrationId: str = ""
    externalId: str = ""
    displayName: str = ""
    avatarUrl: str = ""
    lastSeen: str = ""
    linkedAt: str = ""
    raw: dict | None = None
    info: dict | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("sunco_client", self.id)
