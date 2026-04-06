from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AccessRule:
    id: str
    name: str = ""
    conditions: dict = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("access_rule", self.id)
