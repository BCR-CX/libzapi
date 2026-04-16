from __future__ import annotations

from libzapi.application.commands.voice.availability_cmds import UpdateAvailabilityCmd
from libzapi.domain.models.voice.availability import Availability
from libzapi.infrastructure.api_clients.voice.availability_api_client import AvailabilityApiClient


class AvailabilitiesService:
    def __init__(self, client: AvailabilityApiClient) -> None:
        self._client = client

    def get(self, agent_id: int) -> Availability:
        return self._client.get(agent_id=agent_id)

    def update(self, agent_id: int, **kwargs) -> Availability:
        cmd = UpdateAvailabilityCmd(**kwargs)
        return self._client.update(agent_id=agent_id, cmd=cmd)
