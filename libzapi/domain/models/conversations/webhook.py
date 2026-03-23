from __future__ import annotations

from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Webhook:
    id: str
    target: str = ""
    triggers: list[str] = field(default_factory=list)
    secret: str = ""
    version: str = ""
    includeFullUser: bool = False
    includeFullSource: bool = False

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("sunco_webhook", self.id)
