from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AccountGroupAvailability:
    account_id: int
    group_id: int
    channel_group_statuses: dict | None = None
    unified_states: dict | None = None
    version: int | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("account_group_availability", str(self.group_id))
