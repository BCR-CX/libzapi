from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateDigitalLineCmd:
    nickname: str = ""
    line_type: str = ""
    brand_id: int | None = None
    default_group_id: int | None = None
    group_ids: list[int] | None = None


@dataclass(frozen=True, slots=True)
class UpdateDigitalLineCmd:
    nickname: str | None = None
    default_group_id: int | None = None
    group_ids: list[int] | None = None
    recorded: bool | None = None
    transcription: bool | None = None
    schedule_id: int | None = None
    priority: int | None = None
