from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Integration:
    id: str
    type: str = ""
    status: str = ""
    displayName: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("sunco_integration", self.id)
