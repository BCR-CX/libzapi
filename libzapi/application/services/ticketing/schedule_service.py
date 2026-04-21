from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.schedule_cmds import (
    CreateHolidayCmd,
    CreateScheduleCmd,
    UpdateHolidayCmd,
    UpdateIntervalsCmd,
    UpdateScheduleCmd,
)
from libzapi.domain.models.ticketing.schedule import Holiday, Schedule
from libzapi.infrastructure.api_clients.ticketing.schedule_api_client import (
    ScheduleApiClient,
)


class ScheduleService:
    """High-level service using the API client."""

    def __init__(self, client: ScheduleApiClient) -> None:
        self._client = client

    def list_schedules(self) -> Iterable[Schedule]:
        return self._client.list()

    def get_schedule(self, schedule_id: int) -> Schedule:
        return self._client.get(schedule_id=schedule_id)

    def list_holidays(self, schedule_id: int) -> Iterable[Holiday]:
        return self._client.list_holidays(schedule_id=schedule_id)

    def get_holiday(self, schedule_id: int, holiday_id: int) -> Holiday:
        return self._client.get_holiday(
            schedule_id=schedule_id, holiday_id=holiday_id
        )

    def create(self, **fields) -> Schedule:
        return self._client.create(entity=CreateScheduleCmd(**fields))

    def update(self, schedule_id: int, **fields) -> Schedule:
        return self._client.update(
            schedule_id=schedule_id, entity=UpdateScheduleCmd(**fields)
        )

    def delete(self, schedule_id: int) -> None:
        self._client.delete(schedule_id=schedule_id)

    def update_intervals(self, schedule_id: int, intervals) -> Schedule:
        return self._client.update_intervals(
            schedule_id=schedule_id,
            entity=UpdateIntervalsCmd(intervals=intervals),
        )

    def create_holiday(self, schedule_id: int, **fields) -> Holiday:
        return self._client.create_holiday(
            schedule_id=schedule_id, entity=CreateHolidayCmd(**fields)
        )

    def update_holiday(
        self, schedule_id: int, holiday_id: int, **fields
    ) -> Holiday:
        return self._client.update_holiday(
            schedule_id=schedule_id,
            holiday_id=holiday_id,
            entity=UpdateHolidayCmd(**fields),
        )

    def delete_holiday(self, schedule_id: int, holiday_id: int) -> None:
        self._client.delete_holiday(
            schedule_id=schedule_id, holiday_id=holiday_id
        )
