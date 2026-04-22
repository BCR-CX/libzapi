from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.ticketing.organization import Organization
from libzapi.domain.models.ticketing.ticket import Ticket
from libzapi.domain.models.ticketing.user import User
from libzapi.infrastructure.api_clients.ticketing.incremental_export_api_client import (
    IncrementalExportApiClient,
)


class IncrementalExportsService:
    """High-level service for Zendesk Ticketing Incremental Exports."""

    def __init__(self, client: IncrementalExportApiClient) -> None:
        self._client = client

    def tickets(self, start_time: int) -> Iterable[Ticket]:
        return self._client.tickets(start_time=start_time)

    def tickets_cursor(self, start_time: int) -> Iterable[Ticket]:
        return self._client.tickets_cursor(start_time=start_time)

    def ticket_events(self, start_time: int) -> Iterable[dict]:
        return self._client.ticket_events(start_time=start_time)

    def users(self, start_time: int) -> Iterable[User]:
        return self._client.users(start_time=start_time)

    def users_cursor(self, start_time: int) -> Iterable[User]:
        return self._client.users_cursor(start_time=start_time)

    def organizations(self, start_time: int) -> Iterable[Organization]:
        return self._client.organizations(start_time=start_time)

    def sample(self, resource: str, start_time: int) -> dict:
        return self._client.sample(resource=resource, start_time=start_time)
