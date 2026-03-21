from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateArticleCmd:
    title: str = ""
    body: str = ""
    locale: str = "en-us"
    author_id: int | None = None
    comments_disabled: bool = False
    promoted: bool = False
    position: int = 0
    permission_group_id: int | None = None
    user_segment_id: int | None = None
    content_tag_ids: list[str] | None = None
    label_names: list[str] | None = None


@dataclass(frozen=True, slots=True)
class UpdateArticleCmd:
    title: str | None = None
    body: str | None = None
    locale: str | None = None
    author_id: int | None = None
    comments_disabled: bool | None = None
    promoted: bool | None = None
    position: int | None = None
    permission_group_id: int | None = None
    user_segment_id: int | None = None
    content_tag_ids: list[str] | None = None
    label_names: list[str] | None = None
