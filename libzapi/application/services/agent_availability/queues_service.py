from typing import Iterator

from libzapi.application.commands.agent_availability.queue_cmds import CreateQueueCmd, UpdateQueueCmd
from libzapi.domain.models.agent_availability.queue import Queue
from libzapi.infrastructure.api_clients.agent_availability import QueueApiClient


class QueuesService:
    """High-level service using the API client."""

    def __init__(self, client: QueueApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[Queue]:
        return self._client.list()

    def get(self, queue_id: str) -> Queue:
        return self._client.get(queue_id=queue_id)

    def create(self, entity: CreateQueueCmd) -> Queue:
        return self._client.create(entity=entity)

    def update(self, queue_id: str, entity: UpdateQueueCmd) -> Queue:
        return self._client.update(queue_id=queue_id, entity=entity)

    def delete(self, queue_id: str) -> None:
        return self._client.delete(queue_id=queue_id)

    def list_definitions(self) -> dict:
        return self._client.list_definitions()

    def reorder(self, queue_ids: list[str]) -> dict:
        return self._client.reorder(queue_ids=queue_ids)
