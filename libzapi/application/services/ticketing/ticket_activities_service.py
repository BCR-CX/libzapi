from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.ticketing.ticket_activity import TicketActivity
from libzapi.infrastructure.api_clients.ticketing.ticket_activity_api_client import (
    TicketActivityApiClient,
)


class TicketActivitiesService:
    """High-level service for Zendesk Ticket Activities."""

    def __init__(self, client: TicketActivityApiClient) -> None:
        self._client = client

    def list_all(
        self, *, since: str | None = None, include: str | None = None
    ) -> Iterable[TicketActivity]:
        return self._client.list(since=since, include=include)

    def get_by_id(self, activity_id: int) -> TicketActivity:
        return self._client.get(activity_id=activity_id)
