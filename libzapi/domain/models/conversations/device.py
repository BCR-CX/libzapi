from __future__ import annotations

from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Device:
    id: str
    type: str = ""
    guid: str = ""
    clientId: str = ""
    status: str = ""
    integrationId: str = ""
    lastSeen: str = ""
    pushNotificationToken: str = ""
    appVersion: str = ""
    info: dict | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("device", self.id)
