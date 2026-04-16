from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class PermissionPolicy:
    id: str
    role: str = ""
    create: str = ""
    read: str = ""
    update: str = ""
    delete: str = ""
    create_rule_id: str | None = None
    read_rule_id: str | None = None
    update_rule_id: str | None = None
    delete_rule_id: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("permission_policy", self.id)
