import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.wfm.team_cmds import CreateTeamCmd, UpdateTeamCmd
from libzapi.application.services.wfm.teams_service import TeamsService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


def _make_service(client=None):
    client = client or Mock()
    return TeamsService(client), client


class TestList:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.list.return_value = [sentinel.team]
        result = service.list()
        client.list.assert_called_once_with(deleted=False)
        assert result == [sentinel.team]

    def test_with_deleted(self):
        service, client = _make_service()
        client.list.return_value = []
        service.list(deleted=True)
        client.list.assert_called_once_with(deleted=True)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list()


class TestGet:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.get.return_value = sentinel.team
        result = service.get("team-1")
        client.get.assert_called_once_with(team_id="team-1")
        assert result is sentinel.team


class TestCreate:
    def test_delegates_with_cmd(self):
        service, client = _make_service()
        client.create.return_value = sentinel.team
        result = service.create(name="T", description="D", manager_id=1, agents_ids=["a1"])
        client.create.assert_called_once()
        cmd = client.create.call_args.kwargs["cmd"]
        assert isinstance(cmd, CreateTeamCmd)
        assert cmd.name == "T"
        assert result is sentinel.team


class TestUpdate:
    def test_delegates_with_cmd(self):
        service, client = _make_service()
        client.update.return_value = sentinel.team
        result = service.update("team-1", name="New")
        client.update.assert_called_once()
        cmd = client.update.call_args.kwargs["cmd"]
        assert isinstance(cmd, UpdateTeamCmd)
        assert cmd.name == "New"
        assert result is sentinel.team


class TestDelete:
    def test_delegates_to_client(self):
        service, client = _make_service()
        service.delete("team-1")
        client.delete.assert_called_once_with(team_id="team-1")


class TestRestore:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.restore.return_value = sentinel.team
        result = service.restore("team-1")
        client.restore.assert_called_once_with(team_id="team-1")
        assert result is sentinel.team


class TestBulkAddAgents:
    def test_delegates_with_cmd(self):
        service, client = _make_service()
        client.bulk_add_agents.return_value = sentinel.result
        result = service.bulk_add_agents(agent_ids=["a1"], team_ids=["t1"])
        client.bulk_add_agents.assert_called_once()
        assert result is sentinel.result


class TestBulkRemoveAgents:
    def test_delegates_with_cmd(self):
        service, client = _make_service()
        client.bulk_remove_agents.return_value = sentinel.result
        result = service.bulk_remove_agents(agent_ids=["a1"], team_ids=["t1"])
        client.bulk_remove_agents.assert_called_once()
        assert result is sentinel.result
