from __future__ import annotations

from libzapi.application.commands.voice.availability_cmds import UpdateAvailabilityCmd
from libzapi.domain.models.voice.availability import Availability
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.availability_mapper import to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/availabilities"


class AvailabilityApiClient:
    """HTTP adapter for Zendesk Voice Agent Availability"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, agent_id: int) -> Availability:
        data = self._http.get(f"{_BASE}/{int(agent_id)}")
        return to_domain(data=data["availability"], cls=Availability)

    def update(self, agent_id: int, cmd: UpdateAvailabilityCmd) -> Availability:
        payload = to_payload_update(cmd)
        data = self._http.put(f"{_BASE}/{int(agent_id)}", json=payload)
        return to_domain(data=data["availability"], cls=Availability)
