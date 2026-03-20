from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class CapacityRule:
    id: str
    name: str
    description: str | None = None
    default: bool = False
    capacities: dict | None = None
    assignees: dict | None = None
    created_at: str | None = None
    last_updated_at: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        base = self.name.lower().replace(" ", "_")
        return LogicalKey("capacity_rule", base)
