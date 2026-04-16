from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UpdateAvailabilityCmd:
    agent_state: str | None = None
    call_status: str | None = None
    via: str | None = None
