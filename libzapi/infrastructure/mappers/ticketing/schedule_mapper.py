from __future__ import annotations

from datetime import date

from libzapi.application.commands.ticketing.schedule_cmds import (
    CreateHolidayCmd,
    CreateScheduleCmd,
    UpdateHolidayCmd,
    UpdateIntervalsCmd,
    UpdateScheduleCmd,
)


def _format_date(value: date | str) -> str:
    return value.isoformat() if isinstance(value, date) else value


def to_payload_create_schedule(cmd: CreateScheduleCmd) -> dict:
    body: dict = {"name": cmd.name, "time_zone": cmd.time_zone}
    if cmd.intervals is not None:
        body["intervals"] = list(cmd.intervals)
    return {"schedule": body}


def to_payload_update_schedule(cmd: UpdateScheduleCmd) -> dict:
    body: dict = {}
    if cmd.name is not None:
        body["name"] = cmd.name
    if cmd.time_zone is not None:
        body["time_zone"] = cmd.time_zone
    return {"schedule": body}


def to_payload_update_intervals(cmd: UpdateIntervalsCmd) -> dict:
    return {"workweek": {"intervals": list(cmd.intervals)}}


def to_payload_create_holiday(cmd: CreateHolidayCmd) -> dict:
    return {
        "holiday": {
            "name": cmd.name,
            "start_date": _format_date(cmd.start_date),
            "end_date": _format_date(cmd.end_date),
        }
    }


def to_payload_update_holiday(cmd: UpdateHolidayCmd) -> dict:
    body: dict = {}
    if cmd.name is not None:
        body["name"] = cmd.name
    if cmd.start_date is not None:
        body["start_date"] = _format_date(cmd.start_date)
    if cmd.end_date is not None:
        body["end_date"] = _format_date(cmd.end_date)
    return {"holiday": body}
