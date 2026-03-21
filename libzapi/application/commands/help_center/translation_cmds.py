from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateTranslationCmd:
    locale: str = ""
    title: str = ""
    body: str = ""
    draft: bool = False
    outdated: bool = False


@dataclass(frozen=True, slots=True)
class UpdateTranslationCmd:
    title: str | None = None
    body: str | None = None
    draft: bool | None = None
    outdated: bool | None = None
