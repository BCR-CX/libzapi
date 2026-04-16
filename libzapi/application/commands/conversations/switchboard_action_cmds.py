from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PassControlCmd:
    switchboardIntegration: str
    metadata: dict | None = None


@dataclass(frozen=True, slots=True)
class OfferControlCmd:
    switchboardIntegration: str
    metadata: dict | None = None
