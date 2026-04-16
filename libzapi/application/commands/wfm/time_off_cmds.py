from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ImportTimeOffEntry:
    agentId: int
    startTime: int
    endTime: int
    reasonId: str
    id: str | None = None
    note: str | None = None
    status: str | None = None
    timeOffType: str | None = None


@dataclass(frozen=True, slots=True)
class ImportTimeOffCmd:
    data: list[ImportTimeOffEntry] = field(default_factory=list)
