from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreatePermissionGroupCmd:
    name: str = ""
    edit: list[int] | None = None
    publish: list[int] | None = None


@dataclass(frozen=True, slots=True)
class UpdatePermissionGroupCmd:
    name: str | None = None
    edit: list[int] | None = None
    publish: list[int] | None = None
