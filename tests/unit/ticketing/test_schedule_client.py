import pytest

from libzapi.application.commands.ticketing.schedule_cmds import (
    CreateHolidayCmd,
    CreateScheduleCmd,
    UpdateHolidayCmd,
    UpdateIntervalsCmd,
    UpdateScheduleCmd,
)
from libzapi.infrastructure.api_clients.ticketing import ScheduleApiClient


_INTERVAL = [{"start_time": 1860, "end_time": 2280}]


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.schedule_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.schedule_api_client.yield_items"
    )


# ---------------------------------------------------------------------------
# Schedule / Holiday reads
# ---------------------------------------------------------------------------


def test_list_schedules_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}, {"id": 2}])
    client = ScheduleApiClient(http)
    result = list(client.list())
    assert [r["id"] for r in result] == [1, 2]
    assert all(r["_cls"] == "Schedule" for r in result)
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/business_hours/schedules"
    assert kwargs["items_key"] == "schedules"


def test_list_holidays_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 9}])
    client = ScheduleApiClient(http)
    result = list(client.list_holidays(schedule_id=5))
    assert result[0]["_cls"] == "Holiday"
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/business_hours/schedules/5/holidays"
    assert kwargs["items_key"] == "holidays"


def test_get_schedule_reads_schedule_key(http, domain):
    http.get.return_value = {"schedule": {"id": 1, "name": "P"}}
    client = ScheduleApiClient(http)
    result = client.get(schedule_id=1)
    http.get.assert_called_with("/api/v2/business_hours/schedules/1")
    assert result["_cls"] == "Schedule"
    assert result["name"] == "P"


def test_get_holiday_reads_holiday_key(http, domain):
    http.get.return_value = {"holiday": {"id": 9, "name": "H"}}
    client = ScheduleApiClient(http)
    result = client.get_holiday(schedule_id=5, holiday_id=9)
    http.get.assert_called_with(
        "/api/v2/business_hours/schedules/5/holidays/9"
    )
    assert result["_cls"] == "Holiday"
    assert result["name"] == "H"


# ---------------------------------------------------------------------------
# Schedule CUD
# ---------------------------------------------------------------------------


def test_create_schedule_posts_payload(http, domain):
    http.post.return_value = {"schedule": {"id": 1, "name": "P"}}
    client = ScheduleApiClient(http)
    result = client.create(CreateScheduleCmd(name="P", time_zone="UTC"))
    http.post.assert_called_with(
        "/api/v2/business_hours/schedules",
        {"schedule": {"name": "P", "time_zone": "UTC"}},
    )
    assert result["name"] == "P"


def test_update_schedule_puts_payload(http, domain):
    http.put.return_value = {"schedule": {"id": 1, "name": "N"}}
    client = ScheduleApiClient(http)
    client.update(schedule_id=1, entity=UpdateScheduleCmd(name="N"))
    http.put.assert_called_with(
        "/api/v2/business_hours/schedules/1", {"schedule": {"name": "N"}}
    )


def test_delete_schedule_calls_delete(http):
    client = ScheduleApiClient(http)
    client.delete(schedule_id=7)
    http.delete.assert_called_with("/api/v2/business_hours/schedules/7")


def test_update_intervals_puts_payload(http, domain):
    http.put.return_value = {"schedule": {"id": 1}}
    client = ScheduleApiClient(http)
    client.update_intervals(
        schedule_id=1, entity=UpdateIntervalsCmd(intervals=_INTERVAL)
    )
    http.put.assert_called_with(
        "/api/v2/business_hours/schedules/1/workweek",
        {"workweek": {"intervals": _INTERVAL}},
    )


# ---------------------------------------------------------------------------
# Holiday CUD
# ---------------------------------------------------------------------------


def test_create_holiday_posts_payload(http, domain):
    http.post.return_value = {"holiday": {"id": 9}}
    client = ScheduleApiClient(http)
    client.create_holiday(
        schedule_id=5,
        entity=CreateHolidayCmd(
            name="H", start_date="2026-01-01", end_date="2026-01-02"
        ),
    )
    http.post.assert_called_with(
        "/api/v2/business_hours/schedules/5/holidays",
        {
            "holiday": {
                "name": "H",
                "start_date": "2026-01-01",
                "end_date": "2026-01-02",
            }
        },
    )


def test_update_holiday_puts_payload(http, domain):
    http.put.return_value = {"holiday": {"id": 9}}
    client = ScheduleApiClient(http)
    client.update_holiday(
        schedule_id=5, holiday_id=9, entity=UpdateHolidayCmd(name="H2")
    )
    http.put.assert_called_with(
        "/api/v2/business_hours/schedules/5/holidays/9",
        {"holiday": {"name": "H2"}},
    )


def test_delete_holiday_calls_delete(http):
    client = ScheduleApiClient(http)
    client.delete_holiday(schedule_id=5, holiday_id=9)
    http.delete.assert_called_with(
        "/api/v2/business_hours/schedules/5/holidays/9"
    )
