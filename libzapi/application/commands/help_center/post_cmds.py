from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreatePostCmd:
    title: str = ""
    details: str = ""
    topic_id: int = 0
    content_tag_ids: list[str] | None = None
    notify_subscribers: bool = True


@dataclass(frozen=True, slots=True)
class UpdatePostCmd:
    title: str | None = None
    details: str | None = None
    topic_id: int | None = None
    content_tag_ids: list[str] | None = None
