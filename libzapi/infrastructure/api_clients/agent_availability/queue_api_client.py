from __future__ import annotations
from typing import Iterable

from libzapi.application.commands.agent_availability.queue_cmds import CreateQueueCmd, UpdateQueueCmd
from libzapi.domain.models.agent_availability.queue import Queue
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.agent_availability.queue_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/queues"


class QueueApiClient:
    """HTTP adapter for Zendesk Omnichannel Queues."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterable[Queue]:
        data = self._http.get(_BASE)
        for obj in data.get("queues", []):
            yield to_domain(data=obj, cls=Queue)

    def get(self, queue_id: str) -> Queue:
        data = self._http.get(f"{_BASE}/{queue_id}")
        return to_domain(data=data["queue"], cls=Queue)

    def create(self, entity: CreateQueueCmd) -> Queue:
        payload = to_payload_create(entity)
        data = self._http.post(_BASE, payload)
        return to_domain(data=data["queue"], cls=Queue)

    def update(self, queue_id: str, entity: UpdateQueueCmd) -> Queue:
        payload = to_payload_update(entity)
        data = self._http.put(f"{_BASE}/{queue_id}", payload)
        return to_domain(data=data["queue"], cls=Queue)

    def delete(self, queue_id: str) -> None:
        self._http.delete(f"{_BASE}/{queue_id}")

    def list_definitions(self) -> dict:
        return self._http.get(f"{_BASE}/definitions")

    def reorder(self, queue_ids: list[str]) -> dict:
        return self._http.patch(f"{_BASE}/order", {"queue_ids": queue_ids})
