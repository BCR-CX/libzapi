from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AgentAvailability:
    id: str
    agent_id: int
    agent_status: dict | None = None
    group_ids: list[int] = field(default_factory=list)
    skills: list[int] = field(default_factory=list)
    version: int | None = None
    channels: list[dict] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("agent_availability", str(self.agent_id))
