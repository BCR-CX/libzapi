from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FetchShiftsCmd:
    startDate: str
    endDate: str
    agentIds: list[int] | None = None
    published: int | None = None
    page: int = 1
