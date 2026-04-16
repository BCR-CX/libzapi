from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class IvrRoute:
    id: int
    action: str = ""
    keypress: str = ""
    greeting_id: int | None = None
    options: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("ivr_route", str(self.id))


@dataclass(frozen=True, slots=True)
class IvrMenu:
    id: int
    name: str = ""
    default: bool = False
    greeting_id: int | None = None
    routes: list[IvrRoute] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("ivr_menu", str(self.id))


@dataclass(frozen=True, slots=True)
class Ivr:
    id: int
    name: str = ""
    phone_number_ids: list[int] = field(default_factory=list)
    phone_number_names: list[str] = field(default_factory=list)
    menus: list[IvrMenu] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("ivr", str(self.id))
