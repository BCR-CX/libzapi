from typing import Iterator

from libzapi.domain.models.agent_availability.engagement import Engagement
from libzapi.infrastructure.api_clients.agent_availability import EngagementApiClient


class EngagementsService:
    """High-level service using the API client."""

    def __init__(self, client: EngagementApiClient) -> None:
        self._client = client

    def list_all(
        self,
        agent_id: int | None = None,
        channel: str | None = None,
        ticket_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        filter_by: str | None = None,
        page_size: int | None = None,
    ) -> Iterator[Engagement]:
        return self._client.list(
            agent_id=agent_id,
            channel=channel,
            ticket_id=ticket_id,
            start_time=start_time,
            end_time=end_time,
            filter_by=filter_by,
            page_size=page_size,
        )

    def get(self, engagement_id: str) -> Engagement:
        return self._client.get(engagement_id=engagement_id)
