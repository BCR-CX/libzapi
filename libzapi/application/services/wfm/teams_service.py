from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.wfm.team_cmds import BulkAgentsCmd, CreateTeamCmd, UpdateTeamCmd
from libzapi.domain.models.wfm.team import BulkAgentsResult, Team
from libzapi.infrastructure.api_clients.wfm import TeamApiClient


class TeamsService:
    def __init__(self, client: TeamApiClient) -> None:
        self._client = client

    def list(self, deleted: bool = False) -> Iterable[Team]:
        return self._client.list(deleted=deleted)

    def get(self, team_id: str) -> Team:
        return self._client.get(team_id=team_id)

    def create(self, name: str, description: str, manager_id: int, agents_ids: list[str]) -> Team:
        cmd = CreateTeamCmd(name=name, description=description, manager_id=manager_id, agents_ids=agents_ids)
        return self._client.create(cmd=cmd)

    def update(self, team_id: str, **kwargs) -> Team:
        cmd = UpdateTeamCmd(**kwargs)
        return self._client.update(team_id=team_id, cmd=cmd)

    def delete(self, team_id: str) -> None:
        self._client.delete(team_id=team_id)

    def restore(self, team_id: str) -> Team:
        return self._client.restore(team_id=team_id)

    def bulk_add_agents(self, agent_ids: list[str], team_ids: list[str]) -> BulkAgentsResult:
        cmd = BulkAgentsCmd(agent_ids=agent_ids, team_ids=team_ids)
        return self._client.bulk_add_agents(cmd=cmd)

    def bulk_remove_agents(self, agent_ids: list[str], team_ids: list[str]) -> BulkAgentsResult:
        cmd = BulkAgentsCmd(agent_ids=agent_ids, team_ids=team_ids)
        return self._client.bulk_remove_agents(cmd=cmd)
