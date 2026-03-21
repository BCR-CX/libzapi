from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class UserSubscription:
    id: int
    user_id: int
    content_id: int
    content_type: str | None = None
    locale: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        base = f"id_{self.id}"
        return LogicalKey("user_subscription", base)
