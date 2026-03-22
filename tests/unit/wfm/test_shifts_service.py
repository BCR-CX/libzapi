import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.wfm.shift_cmds import FetchShiftsCmd
from libzapi.application.services.wfm.shifts_service import ShiftsService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


def _make_service(client=None):
    client = client or Mock()
    return ShiftsService(client), client


class TestFetch:
    def test_delegates_to_client_with_cmd(self):
        service, client = _make_service()
        client.fetch.return_value = [sentinel.shift]
        result = service.fetch(start_date="2024-01-01", end_date="2024-01-31")
        client.fetch.assert_called_once()
        cmd = client.fetch.call_args.kwargs["cmd"]
        assert isinstance(cmd, FetchShiftsCmd)
        assert cmd.startDate == "2024-01-01"
        assert cmd.endDate == "2024-01-31"
        assert result == [sentinel.shift]

    def test_passes_optional_fields(self):
        service, client = _make_service()
        client.fetch.return_value = []
        service.fetch(start_date="2024-01-01", end_date="2024-01-31", agent_ids=[1, 2], published=1, page=2)
        cmd = client.fetch.call_args.kwargs["cmd"]
        assert cmd.agentIds == [1, 2]
        assert cmd.published == 1
        assert cmd.page == 2

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_propagates_error(self, error_cls):
        service, client = _make_service()
        client.fetch.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.fetch(start_date="2024-01-01", end_date="2024-01-31")
