from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateBadgeCmd:
    badge_category_id: str = ""
    name: str = ""
    description: str = ""


@dataclass(frozen=True, slots=True)
class UpdateBadgeCmd:
    name: str | None = None
    description: str | None = None
    badge_category_id: str | None = None
