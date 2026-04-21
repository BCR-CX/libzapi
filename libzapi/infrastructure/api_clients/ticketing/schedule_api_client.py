from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.schedule_cmds import (
    CreateHolidayCmd,
    CreateScheduleCmd,
    UpdateHolidayCmd,
    UpdateIntervalsCmd,
    UpdateScheduleCmd,
)
from libzapi.domain.models.ticketing.schedule import Holiday, Schedule
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.schedule_mapper import (
    to_payload_create_holiday,
    to_payload_create_schedule,
    to_payload_update_holiday,
    to_payload_update_intervals,
    to_payload_update_schedule,
)
from libzapi.infrastructure.serialization.parse import to_domain


class ScheduleApiClient:
    """HTTP adapter for Zendesk Schedules with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Schedule]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/business_hours/schedules",
            base_url=self._http.base_url,
            items_key="schedules",
        ):
            yield to_domain(data=obj, cls=Schedule)

    def list_holidays(self, schedule_id: int) -> Iterator[Holiday]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/business_hours/schedules/{int(schedule_id)}/holidays",
            base_url=self._http.base_url,
            items_key="holidays",
        ):
            yield to_domain(data=obj, cls=Holiday)

    def get(self, schedule_id: int) -> Schedule:
        data = self._http.get(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}"
        )
        return to_domain(data=data["schedule"], cls=Schedule)

    def get_holiday(self, schedule_id: int, holiday_id: int) -> Holiday:
        data = self._http.get(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}/holidays/{int(holiday_id)}"
        )
        return to_domain(data=data["holiday"], cls=Holiday)

    def create(self, entity: CreateScheduleCmd) -> Schedule:
        payload = to_payload_create_schedule(entity)
        data = self._http.post("/api/v2/business_hours/schedules", payload)
        return to_domain(data=data["schedule"], cls=Schedule)

    def update(self, schedule_id: int, entity: UpdateScheduleCmd) -> Schedule:
        payload = to_payload_update_schedule(entity)
        data = self._http.put(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}", payload
        )
        return to_domain(data=data["schedule"], cls=Schedule)

    def delete(self, schedule_id: int) -> None:
        self._http.delete(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}"
        )

    def update_intervals(
        self, schedule_id: int, entity: UpdateIntervalsCmd
    ) -> Schedule:
        payload = to_payload_update_intervals(entity)
        data = self._http.put(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}/workweek",
            payload,
        )
        return to_domain(data=data["schedule"], cls=Schedule)

    def create_holiday(
        self, schedule_id: int, entity: CreateHolidayCmd
    ) -> Holiday:
        payload = to_payload_create_holiday(entity)
        data = self._http.post(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}/holidays",
            payload,
        )
        return to_domain(data=data["holiday"], cls=Holiday)

    def update_holiday(
        self, schedule_id: int, holiday_id: int, entity: UpdateHolidayCmd
    ) -> Holiday:
        payload = to_payload_update_holiday(entity)
        data = self._http.put(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}/holidays/{int(holiday_id)}",
            payload,
        )
        return to_domain(data=data["holiday"], cls=Holiday)

    def delete_holiday(self, schedule_id: int, holiday_id: int) -> None:
        self._http.delete(
            f"/api/v2/business_hours/schedules/{int(schedule_id)}/holidays/{int(holiday_id)}"
        )
