from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateSwitchboardCmd:
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class UpdateSwitchboardCmd:
    enabled: bool | None = None
    defaultSwitchboardIntegrationId: str | None = None


@dataclass(frozen=True, slots=True)
class CreateSwitchboardIntegrationCmd:
    name: str
    integrationId: str
    integrationType: str = ""
    deliverStandbyEvents: bool = False


@dataclass(frozen=True, slots=True)
class UpdateSwitchboardIntegrationCmd:
    name: str | None = None
    deliverStandbyEvents: bool | None = None
    nextSwitchboardIntegrationId: str | None = None
    messageHistoryCount: int | None = None
