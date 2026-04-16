from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateGreetingCmd:
    category_id: int
    name: str
    audio_name: str = ""


@dataclass(frozen=True, slots=True)
class UpdateGreetingCmd:
    name: str | None = None
