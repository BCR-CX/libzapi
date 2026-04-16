from __future__ import annotations

from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class User:
    id: str
    externalId: str = ""
    zendeskId: str = ""
    signedUpAt: str = ""
    profile: dict | None = None
    metadata: dict | None = None
    authenticated: bool = False
    identities: list[dict] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("sunco_user", self.id)
