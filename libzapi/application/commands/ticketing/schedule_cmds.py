from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateScheduleCmd:
    name: str
    time_zone: str
    intervals: Iterable[dict[str, Any]] | None = None


@dataclass(frozen=True, slots=True)
class UpdateScheduleCmd:
    name: str | None = None
    time_zone: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateIntervalsCmd:
    intervals: Iterable[dict[str, Any]]


@dataclass(frozen=True, slots=True)
class CreateHolidayCmd:
    name: str
    start_date: date | str
    end_date: date | str


@dataclass(frozen=True, slots=True)
class UpdateHolidayCmd:
    name: str | None = None
    start_date: date | str | None = None
    end_date: date | str | None = None


ScheduleCmd: TypeAlias = CreateScheduleCmd | UpdateScheduleCmd
HolidayCmd: TypeAlias = CreateHolidayCmd | UpdateHolidayCmd
