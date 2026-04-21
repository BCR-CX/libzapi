from datetime import date

from libzapi.application.commands.ticketing.schedule_cmds import (
    CreateHolidayCmd,
    CreateScheduleCmd,
    UpdateHolidayCmd,
    UpdateIntervalsCmd,
    UpdateScheduleCmd,
)
from libzapi.infrastructure.mappers.ticketing.schedule_mapper import (
    to_payload_create_holiday,
    to_payload_create_schedule,
    to_payload_update_holiday,
    to_payload_update_intervals,
    to_payload_update_schedule,
)


_INTERVAL = [{"start_time": 1860, "end_time": 2280}]


# ---------------------------------------------------------------------------
# Schedule create / update
# ---------------------------------------------------------------------------


def test_create_schedule_minimal_payload():
    payload = to_payload_create_schedule(
        CreateScheduleCmd(name="Primary", time_zone="UTC")
    )
    assert payload == {
        "schedule": {"name": "Primary", "time_zone": "UTC"}
    }


def test_create_schedule_with_intervals():
    body = to_payload_create_schedule(
        CreateScheduleCmd(name="P", time_zone="UTC", intervals=_INTERVAL)
    )["schedule"]
    assert body["intervals"] == _INTERVAL


def test_create_schedule_converts_intervals_iterable():
    body = to_payload_create_schedule(
        CreateScheduleCmd(name="P", time_zone="UTC", intervals=iter(_INTERVAL))
    )["schedule"]
    assert body["intervals"] == _INTERVAL


def test_update_schedule_empty_patch():
    assert to_payload_update_schedule(UpdateScheduleCmd()) == {"schedule": {}}


def test_update_schedule_includes_fields():
    body = to_payload_update_schedule(
        UpdateScheduleCmd(name="N", time_zone="UTC")
    )["schedule"]
    assert body == {"name": "N", "time_zone": "UTC"}


# ---------------------------------------------------------------------------
# Intervals
# ---------------------------------------------------------------------------


def test_update_intervals_wraps_in_workweek():
    payload = to_payload_update_intervals(
        UpdateIntervalsCmd(intervals=_INTERVAL)
    )
    assert payload == {"workweek": {"intervals": _INTERVAL}}


def test_update_intervals_converts_iterable():
    payload = to_payload_update_intervals(
        UpdateIntervalsCmd(intervals=iter(_INTERVAL))
    )
    assert payload == {"workweek": {"intervals": _INTERVAL}}


# ---------------------------------------------------------------------------
# Holiday create / update
# ---------------------------------------------------------------------------


def test_create_holiday_formats_dates():
    payload = to_payload_create_holiday(
        CreateHolidayCmd(
            name="H",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 2),
        )
    )
    assert payload == {
        "holiday": {
            "name": "H",
            "start_date": "2026-01-01",
            "end_date": "2026-01-02",
        }
    }


def test_create_holiday_accepts_string_dates():
    payload = to_payload_create_holiday(
        CreateHolidayCmd(name="H", start_date="2026-01-01", end_date="2026-01-02")
    )
    assert payload["holiday"]["start_date"] == "2026-01-01"


def test_update_holiday_empty_patch():
    assert to_payload_update_holiday(UpdateHolidayCmd()) == {"holiday": {}}


def test_update_holiday_includes_all_fields():
    payload = to_payload_update_holiday(
        UpdateHolidayCmd(
            name="H2",
            start_date=date(2026, 3, 1),
            end_date=date(2026, 3, 2),
        )
    )
    assert payload == {
        "holiday": {
            "name": "H2",
            "start_date": "2026-03-01",
            "end_date": "2026-03-02",
        }
    }


def test_update_holiday_partial():
    payload = to_payload_update_holiday(UpdateHolidayCmd(name="Only"))
    assert payload == {"holiday": {"name": "Only"}}
