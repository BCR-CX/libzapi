from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateBadgeCategoryCmd:
    brand_id: int = 0
    name: str = ""
    slug: str = ""
