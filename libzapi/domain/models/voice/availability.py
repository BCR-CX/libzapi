from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Availability:
    agent_state: str = ""
    call_status: str | None = None
    via: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("availability", self.agent_state)
