from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Greeting:
    id: str
    name: str = ""
    category_id: int | None = None
    active: bool = False
    default: bool = False
    audio_name: str = ""
    audio_url: str = ""
    phone_number_ids: list[int] = field(default_factory=list)
    ivr_ids: list[int] = field(default_factory=list)
    upload_id: int | None = None
    pending: bool = False

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("greeting", str(self.id))


@dataclass(frozen=True, slots=True)
class GreetingCategory:
    id: int
    name: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("greeting_category", str(self.id))
