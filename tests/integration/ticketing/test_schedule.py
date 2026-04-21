import uuid
from datetime import date

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_schedule(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        name=f"libzapi schedule {suffix}",
        time_zone="Eastern Time (US & Canada)",
    )
    defaults.update(overrides)
    return ticketing.schedules.create(**defaults)


def test_list_and_get_schedule(ticketing: Ticketing):
    schedules = list(ticketing.schedules.list_schedules())
    assert isinstance(schedules, list)
    if schedules:
        schedule = ticketing.schedules.get_schedule(schedules[0].id)
        assert schedule.id == schedules[0].id


def test_create_update_delete_schedule(ticketing: Ticketing):
    schedule = _create_schedule(ticketing)
    try:
        assert schedule.id > 0
        updated = ticketing.schedules.update(
            schedule.id, name=f"libzapi updated {_unique()}"
        )
        assert updated.name.startswith("libzapi updated")
    finally:
        ticketing.schedules.delete(schedule.id)


def test_update_intervals(ticketing: Ticketing):
    schedule = _create_schedule(ticketing)
    try:
        intervals = [
            {"start_time": 1860, "end_time": 2280},
            {"start_time": 3300, "end_time": 3720},
        ]
        result = ticketing.schedules.update_intervals(
            schedule_id=schedule.id, intervals=intervals
        )
        assert result.id == schedule.id
    finally:
        ticketing.schedules.delete(schedule.id)


def test_holiday_lifecycle(ticketing: Ticketing):
    schedule = _create_schedule(ticketing)
    try:
        holiday = ticketing.schedules.create_holiday(
            schedule_id=schedule.id,
            name=f"libzapi holiday {_unique()}",
            start_date=date(2030, 1, 1),
            end_date=date(2030, 1, 2),
        )
        assert holiday.id > 0

        fetched = ticketing.schedules.get_holiday(
            schedule.id, holiday.id
        )
        assert fetched.id == holiday.id

        listed = list(ticketing.schedules.list_holidays(schedule.id))
        assert any(h.id == holiday.id for h in listed)

        updated = ticketing.schedules.update_holiday(
            schedule.id, holiday.id, name=f"libzapi updated {_unique()}"
        )
        assert updated.name.startswith("libzapi updated")

        ticketing.schedules.delete_holiday(schedule.id, holiday.id)
    finally:
        ticketing.schedules.delete(schedule.id)
