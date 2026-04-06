from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateCustomObjectCmd:
    key: str
    title: str
    title_pluralized: str
    include_in_list_view: bool = False
    description: str = ""
    allows_photos: bool = False
    allows_attachments: bool = False


@dataclass(frozen=True, slots=True)
class UpdateCustomObjectCmd:
    title: str | None = None
    title_pluralized: str | None = None
    description: str | None = None
    include_in_list_view: bool | None = None
    allows_photos: bool | None = None
    allows_attachments: bool | None = None
