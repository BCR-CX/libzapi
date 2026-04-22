from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateBookmarkCmd:
    ticket_id: int
