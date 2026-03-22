from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class TimeOffReason:
    id: str
    name: str
    type: str = ""
    deletedAt: str | None = None
    isDeleted: bool = False


@dataclass(frozen=True, slots=True)
class TimeOffStatusHistory:
    id: str
    timeOffId: str = ""
    status: str = ""
    tymeshiftAccountId: int | None = None
    note: str | None = None
    internalNote: str | None = None
    auto: bool = False
    createdAt: str = ""
    createdBy: int | None = None


@dataclass(frozen=True, slots=True)
class TimeOff:
    timeOffRequestId: str
    agentId: int
    startTime: int
    endTime: int
    status: str = ""
    timeOffType: str = ""
    auto: bool = False
    note: str | None = None
    reasonId: str = ""
    reason: TimeOffReason | None = None
    statusHistory: list[TimeOffStatusHistory] = field(default_factory=list)
    createdAt: int | None = None
    source: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("wfm_time_off", self.timeOffRequestId)


@dataclass(frozen=True, slots=True)
class TimeOffImportResult:
    entities: list[dict] = field(default_factory=list)
    inserted: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
