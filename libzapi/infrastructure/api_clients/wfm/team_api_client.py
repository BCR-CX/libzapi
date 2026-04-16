from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.wfm.team_cmds import BulkAgentsCmd, CreateTeamCmd, UpdateTeamCmd
from libzapi.domain.models.wfm.team import BulkAgentsResult, Team
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.wfm.team_mapper import to_payload_bulk_agents, to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/wfm/l5/api/v2/teams"


class TeamApiClient:
    """HTTP adapter for WFM Teams API."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, deleted: bool = False) -> Iterable[Team]:
        path = f"{_BASE}?deleted=true" if deleted else _BASE
        data = self._http.get(path)
        for item in data.get("teams", []):
            yield to_domain(data=item, cls=Team)

    def get(self, team_id: str) -> Team:
        data = self._http.get(f"{_BASE}/{team_id}")
        return to_domain(data=data, cls=Team)

    def create(self, cmd: CreateTeamCmd) -> Team:
        payload = to_payload_create(cmd)
        data = self._http.post(_BASE, json=payload)
        return to_domain(data=data, cls=Team)

    def update(self, team_id: str, cmd: UpdateTeamCmd) -> Team:
        payload = to_payload_update(cmd)
        data = self._http.put(f"{_BASE}/{team_id}", json=payload)
        return to_domain(data=data, cls=Team)

    def delete(self, team_id: str) -> None:
        self._http.delete(f"{_BASE}/{team_id}")

    def restore(self, team_id: str) -> Team:
        data = self._http.post(f"{_BASE}/restore", json={"id": team_id})
        return to_domain(data=data, cls=Team)

    def bulk_add_agents(self, cmd: BulkAgentsCmd) -> BulkAgentsResult:
        payload = to_payload_bulk_agents(cmd)
        data = self._http.post(f"{_BASE}/bulk/add_agents", json=payload)
        return to_domain(data=data, cls=BulkAgentsResult)

    def bulk_remove_agents(self, cmd: BulkAgentsCmd) -> BulkAgentsResult:
        payload = to_payload_bulk_agents(cmd)
        data = self._http.post(f"{_BASE}/bulk/remove_agents", json=payload)
        return to_domain(data=data, cls=BulkAgentsResult)
