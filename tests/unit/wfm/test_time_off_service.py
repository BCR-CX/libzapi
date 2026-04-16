import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.wfm.time_off_cmds import ImportTimeOffEntry
from libzapi.application.services.wfm.time_off_service import TimeOffService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


def _make_service(client=None):
    client = client or Mock()
    return TimeOffService(client), client


class TestList:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.list.return_value = [sentinel.time_off]
        result = service.list(agent_id=42, status="approved")
        client.list.assert_called_once_with(
            time_off_request_id=None,
            agent_id=42,
            start_time=None,
            end_time=None,
            status="approved",
            reason_id=None,
            time_off_type=None,
            page=None,
            per_page=None,
        )
        assert result == [sentinel.time_off]

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list()


class TestImport:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.import_time_off.return_value = sentinel.result
        entry = ImportTimeOffEntry(agentId=1, startTime=100, endTime=200, reasonId="r1")
        result = service.import_time_off(entries=[entry])
        client.import_time_off.assert_called_once()
        cmd = client.import_time_off.call_args.kwargs["cmd"]
        assert len(cmd.data) == 1
        assert cmd.data[0].agentId == 1
        assert result is sentinel.result

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_propagates_error(self, error_cls):
        service, client = _make_service()
        client.import_time_off.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.import_time_off(entries=[])
