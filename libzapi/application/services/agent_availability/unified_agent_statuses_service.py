from libzapi.domain.models.agent_availability.job_status import JobStatus
from libzapi.domain.models.agent_availability.unified_agent_status import UnifiedAgentStatus
from libzapi.infrastructure.api_clients.agent_availability import UnifiedAgentStatusApiClient


class UnifiedAgentStatusesService:
    """High-level service using the API client."""

    def __init__(self, client: UnifiedAgentStatusApiClient) -> None:
        self._client = client

    def list_all(self) -> list[UnifiedAgentStatus]:
        return self._client.list_all()

    def list_me(self) -> list[UnifiedAgentStatus]:
        return self._client.list_me()

    def update_agent(self, agent_id: int, status_id: int) -> dict:
        return self._client.update_agent(agent_id=agent_id, status_id=status_id)

    def update_me(self, status_id: int) -> dict:
        return self._client.update_me(status_id=status_id)

    def bulk_update(self, agent_ids: list[int], status_id: int) -> dict:
        return self._client.bulk_update(agent_ids=agent_ids, status_id=status_id)

    def get_job_status(self, job_id: str) -> JobStatus:
        return self._client.get_job_status(job_id=job_id)
