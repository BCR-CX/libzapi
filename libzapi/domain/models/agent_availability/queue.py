from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Queue:
    id: str
    name: str
    description: str | None = None
    definition: dict | None = None
    order: int | None = None
    priority: int | None = None
    primary_groups: dict | None = None
    secondary_groups: dict | None = None
    created_at: str | None = None
    updated_at: str | None = None
    url: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        base = self.name.lower().replace(" ", "_")
        return LogicalKey("queue", base)
