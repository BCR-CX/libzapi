from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateArticleLabelCmd:
    name: str = ""
