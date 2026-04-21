from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateGroupMembershipCmd:
    user_id: int
    group_id: int
    default: bool | None = None
