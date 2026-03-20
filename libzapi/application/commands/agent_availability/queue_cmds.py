from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateQueueCmd:
    name: str
    definition: dict
    priority: int
    primary_groups: dict
    description: str | None = None
    secondary_groups: dict | None = None


@dataclass(frozen=True, slots=True)
class UpdateQueueCmd:
    name: str | None = None
    description: str | None = None
    definition: dict | None = None
    priority: int | None = None
    primary_groups: dict | None = None
    secondary_groups: dict | None = None
