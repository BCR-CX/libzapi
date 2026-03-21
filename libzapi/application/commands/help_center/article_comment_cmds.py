from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateArticleCommentCmd:
    body: str = ""
    locale: str | None = None
    author_id: int | None = None
    notify_subscribers: bool = True


@dataclass(frozen=True, slots=True)
class UpdateArticleCommentCmd:
    body: str | None = None
