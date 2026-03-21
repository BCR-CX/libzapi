from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreatePostCommentCmd:
    body: str = ""
    notify_subscribers: bool = True


@dataclass(frozen=True, slots=True)
class UpdatePostCommentCmd:
    body: str | None = None
    official: bool | None = None
