from typing import Iterator

from libzapi.domain.models.custom_data.record_event import RecordEvent
from libzapi.infrastructure.api_clients.custom_data import RecordEventApiClient


class RecordEventsService:
    def __init__(self, client: RecordEventApiClient) -> None:
        self._client = client

    def list_all(self, custom_object_key: str, record_id: str, page_size: int = 100) -> Iterator[RecordEvent]:
        return self._client.list_all(custom_object_key=custom_object_key, record_id=record_id, page_size=page_size)
