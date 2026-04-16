from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AgentRef:
    id: int
    name: str
    email: str
    deactivated: bool = False
    isDeleted: bool = False


@dataclass(frozen=True, slots=True)
class ActivityTypeRef:
    id: str
    name: str
    color: str = ""
    isDeleted: bool = False


@dataclass(frozen=True, slots=True)
class Activity:
    id: str
    agentId: int
    startTime: int
    type: str
    name: str = ""
    ticketId: int | None = None
    endTime: int | None = None
    duration: int | None = None
    activityTypeIds: list[str] = field(default_factory=list)
    eventType: str = ""
    color: str = ""
    isPaid: bool = False
    lockIntervals: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("wfm_activity", self.id)
