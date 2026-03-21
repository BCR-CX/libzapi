from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateTopicCmd:
    name: str = ""
    description: str = ""
    position: int = 0
    manageable_by: str | None = None
    user_segment_id: int | None = None


@dataclass(frozen=True, slots=True)
class UpdateTopicCmd:
    name: str | None = None
    description: str | None = None
    position: int | None = None
    manageable_by: str | None = None
    user_segment_id: int | None = None
