from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateContentTagCmd:
    name: str = ""


@dataclass(frozen=True, slots=True)
class UpdateContentTagCmd:
    name: str | None = None
