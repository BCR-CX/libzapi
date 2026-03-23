from __future__ import annotations

from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Conversation:
    id: str
    type: str = ""
    displayName: str = ""
    description: str = ""
    iconUrl: str = ""
    metadata: dict = field(default_factory=dict)
    activeSwitchboardIntegration: dict | None = None
    pendingSwitchboardIntegration: dict | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("conversation", self.id)
