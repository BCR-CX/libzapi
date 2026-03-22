from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class ShiftTask:
    id: str
    startTime: int
    endTime: int
    name: str = ""
    color: str = ""
    taskableId: str = ""
    taskableType: str = ""
    createdAt: str = ""
    note: str = ""


@dataclass(frozen=True, slots=True)
class Shift:
    id: str
    agentId: int
    startTime: int
    endTime: int
    published: bool = False
    parentId: str | int | None = None
    tasks: list[ShiftTask] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("wfm_shift", self.id)
