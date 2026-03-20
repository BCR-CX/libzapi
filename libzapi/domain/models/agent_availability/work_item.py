from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class WorkItem:
    id: str
    added_at: str | None = None
    reason: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("work_item", self.id)
