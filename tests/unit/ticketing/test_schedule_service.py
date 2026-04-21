import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.schedule_cmds import (
    CreateHolidayCmd,
    CreateScheduleCmd,
    UpdateHolidayCmd,
    UpdateIntervalsCmd,
    UpdateScheduleCmd,
)
from libzapi.application.services.ticketing.schedule_service import (
    ScheduleService,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)


_INTERVAL = [{"start_time": 1860, "end_time": 2280}]


def _make_service(client=None):
    client = client or Mock()
    return ScheduleService(client), client


class TestDelegation:
    def test_list_schedules_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.schedules
        assert service.list_schedules() is sentinel.schedules

    def test_get_schedule_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.schedule
        assert service.get_schedule(5) is sentinel.schedule
        client.get.assert_called_once_with(schedule_id=5)

    def test_list_holidays_delegates(self):
        service, client = _make_service()
        client.list_holidays.return_value = sentinel.holidays
        assert service.list_holidays(5) is sentinel.holidays
        client.list_holidays.assert_called_once_with(schedule_id=5)

    def test_get_holiday_delegates(self):
        service, client = _make_service()
        client.get_holiday.return_value = sentinel.holiday
        assert service.get_holiday(5, 9) is sentinel.holiday
        client.get_holiday.assert_called_once_with(schedule_id=5, holiday_id=9)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(schedule_id=5)

    def test_delete_holiday_delegates(self):
        service, client = _make_service()
        service.delete_holiday(5, 9)
        client.delete_holiday.assert_called_once_with(
            schedule_id=5, holiday_id=9
        )


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.schedule

        result = service.create(name="P", time_zone="UTC")

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateScheduleCmd)
        assert cmd.name == "P"
        assert cmd.time_zone == "UTC"
        assert result is sentinel.schedule


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.schedule

        result = service.update(7, name="N")

        assert client.update.call_args.kwargs["schedule_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateScheduleCmd)
        assert cmd.name == "N"
        assert result is sentinel.schedule

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.name is None


class TestUpdateIntervals:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.update_intervals.return_value = sentinel.schedule

        result = service.update_intervals(schedule_id=5, intervals=_INTERVAL)

        assert result is sentinel.schedule
        assert client.update_intervals.call_args.kwargs["schedule_id"] == 5
        cmd = client.update_intervals.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateIntervalsCmd)
        assert list(cmd.intervals) == _INTERVAL


class TestHolidays:
    def test_create_holiday_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create_holiday.return_value = sentinel.holiday

        result = service.create_holiday(
            schedule_id=5,
            name="H",
            start_date="2026-01-01",
            end_date="2026-01-02",
        )

        cmd = client.create_holiday.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateHolidayCmd)
        assert cmd.name == "H"
        assert result is sentinel.holiday

    def test_update_holiday_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.update_holiday.return_value = sentinel.holiday

        result = service.update_holiday(
            schedule_id=5, holiday_id=9, name="H2"
        )

        cmd = client.update_holiday.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateHolidayCmd)
        assert cmd.name == "H2"
        assert result is sentinel.holiday


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(name="P", time_zone="UTC")

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_schedules_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_schedules()
