import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.job_statuses_service import (
    JobStatusesService,
    JobStatusTimeout,
)
from libzapi.domain.errors import NotFound, Unauthorized
from libzapi.domain.shared_objects.job_status import JobStatus


def _make_service(client=None):
    client = client or Mock()
    return JobStatusesService(client), client


def _make_status(status: str) -> JobStatus:
    return JobStatus(
        id="abc",
        job_type="",
        url="",
        total=0,
        progress="",
        status=status,
        message="",
    )


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.iter
        assert service.list_all() is sentinel.iter
        client.list.assert_called_once_with()

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.status
        assert service.get_by_id("abc") is sentinel.status
        client.get.assert_called_once_with(job_id="abc")

    def test_show_many_delegates(self):
        service, client = _make_service()
        client.show_many.return_value = [sentinel.a]
        assert service.show_many(["a", "b"]) == [sentinel.a]
        client.show_many.assert_called_once_with(job_ids=["a", "b"])


class TestWaitUntilComplete:
    def test_returns_immediately_when_already_completed(self):
        service, client = _make_service()
        client.get.return_value = _make_status("completed")
        sleep = Mock()
        result = service.wait_until_complete(
            "abc", interval=0.1, timeout=5.0, sleep=sleep
        )
        assert result.status == "completed"
        sleep.assert_not_called()

    def test_polls_until_terminal_state(self):
        service, client = _make_service()
        client.get.side_effect = [
            _make_status("queued"),
            _make_status("working"),
            _make_status("completed"),
        ]
        sleep = Mock()
        result = service.wait_until_complete(
            "abc", interval=0.1, timeout=5.0, sleep=sleep
        )
        assert result.status == "completed"
        assert sleep.call_count == 2

    @pytest.mark.parametrize("terminal", ["completed", "failed", "killed"])
    def test_treats_failed_and_killed_as_terminal(self, terminal):
        service, client = _make_service()
        client.get.return_value = _make_status(terminal)
        result = service.wait_until_complete(
            "abc", interval=0.1, timeout=5.0, sleep=Mock()
        )
        assert result.status == terminal

    def test_raises_timeout_when_never_terminal(self):
        service, client = _make_service()
        client.get.return_value = _make_status("working")
        # now() returns an ever-growing sequence so deadline is quickly exceeded
        now_values = iter([0.0, 10.0, 20.0])
        with pytest.raises(JobStatusTimeout):
            service.wait_until_complete(
                "abc",
                interval=0.1,
                timeout=5.0,
                sleep=Mock(),
                now=lambda: next(now_values),
            )

    def test_uses_injected_sleep(self):
        service, client = _make_service()
        client.get.side_effect = [
            _make_status("queued"),
            _make_status("completed"),
        ]
        sleep = Mock()
        service.wait_until_complete(
            "abc", interval=0.42, timeout=5.0, sleep=sleep
        )
        sleep.assert_called_once_with(0.42)


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_get_propagates_error(self, error_cls):
        service, client = _make_service()
        client.get.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.get_by_id("abc")
