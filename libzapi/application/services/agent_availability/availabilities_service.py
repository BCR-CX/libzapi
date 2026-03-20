from typing import Iterator

from libzapi.domain.models.agent_availability.agent_availability import AgentAvailability
from libzapi.domain.models.agent_availability.work_item import WorkItem
from libzapi.infrastructure.api_clients.agent_availability import AgentAvailabilityApiClient


class AvailabilitiesService:
    """High-level service using the API client."""

    def __init__(self, client: AgentAvailabilityApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[AgentAvailability]:
        return self._client.list()

    def get(self, agent_id: int) -> AgentAvailability:
        return self._client.get(agent_id=agent_id)

    def get_me(self) -> AgentAvailability:
        return self._client.get_me()

    def work_items(self, agent_id: int, channel: str) -> Iterator[WorkItem]:
        return self._client.work_items(agent_id=agent_id, channel=channel)

    def my_work_items(self, channel: str) -> Iterator[WorkItem]:
        return self._client.my_work_items(channel=channel)
