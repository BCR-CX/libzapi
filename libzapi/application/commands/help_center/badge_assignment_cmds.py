from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateBadgeAssignmentCmd:
    badge_id: str = ""
    user_id: int = 0
