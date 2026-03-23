from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AppKey:
    id: str
    displayName: str = ""
    secret: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("app_key", self.id)
