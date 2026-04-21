from __future__ import annotations

from typing import Any, Iterable

from libzapi.application.commands.ticketing.ticket_trigger_cmds import (
    CreateTicketTriggerCmd,
    UpdateTicketTriggerCmd,
)
from libzapi.domain.models.ticketing.ticket_trigger import TicketTrigger
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing import TicketTriggerApiClient


class TicketTriggerService:
    """High-level service using the API client."""

    def __init__(self, client: TicketTriggerApiClient) -> None:
        self._client = client

    def list(self) -> Iterable[TicketTrigger]:
        return self._client.list()

    def list_active(self) -> Iterable[TicketTrigger]:
        return self._client.list_active()

    def search(self, query: str) -> Iterable[TicketTrigger]:
        return self._client.search(query=query)

    def list_definitions(self) -> dict:
        return self._client.list_definitions()

    def get(self, trigger_id: int) -> TicketTrigger:
        return self._client.get(trigger_id=trigger_id)

    def create(self, **fields) -> TicketTrigger:
        return self._client.create(entity=CreateTicketTriggerCmd(**fields))

    def update(self, trigger_id: int, **fields) -> TicketTrigger:
        return self._client.update(
            trigger_id=trigger_id, entity=UpdateTicketTriggerCmd(**fields)
        )

    def delete(self, trigger_id: int) -> None:
        self._client.delete(trigger_id=trigger_id)

    def create_many(
        self, triggers: Iterable[dict[str, Any]]
    ) -> JobStatus:
        return self._client.create_many(
            entities=[CreateTicketTriggerCmd(**t) for t in triggers]
        )

    def update_many(
        self, updates: Iterable[tuple[int, dict[str, Any]]]
    ) -> JobStatus:
        pairs = [
            (trigger_id, UpdateTicketTriggerCmd(**fields))
            for trigger_id, fields in updates
        ]
        return self._client.update_many(updates=pairs)

    def destroy_many(self, trigger_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(trigger_ids=trigger_ids)
