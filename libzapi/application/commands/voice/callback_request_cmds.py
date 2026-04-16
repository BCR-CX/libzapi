from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CreateCallbackRequestCmd:
    phone_number_id: int
    requester_phone_number: str
    group_ids: list[int] = field(default_factory=list)
