from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class UnifiedAgentStatus:
    id: int
    name: str
    description: str | None = None
    group_ids: list[int] = field(default_factory=list)
    channels: dict | None = None
    updated_at: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        base = self.name.lower().replace(" ", "_")
        return LogicalKey("unified_agent_status", base)
