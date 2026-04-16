from __future__ import annotations

from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Switchboard:
    id: str
    enabled: bool = False
    defaultSwitchboardIntegrationId: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("switchboard", self.id)


@dataclass(frozen=True, slots=True)
class SwitchboardIntegration:
    id: str
    name: str = ""
    integrationId: str = ""
    integrationType: str = ""
    deliverStandbyEvents: bool = False
    nextSwitchboardIntegrationId: str = ""
    messageHistoryCount: int | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("switchboard_integration", self.id)
