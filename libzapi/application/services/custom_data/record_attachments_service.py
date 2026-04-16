from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.custom_data.record_attachment import RecordAttachment
from libzapi.infrastructure.api_clients.custom_data import RecordAttachmentApiClient


class RecordAttachmentsService:
    def __init__(self, client: RecordAttachmentApiClient) -> None:
        self._client = client

    def list_all(self, custom_object_key: str, record_id: str) -> Iterator[RecordAttachment]:
        return self._client.list_all(custom_object_key=custom_object_key, record_id=record_id)

    def create(self, custom_object_key: str, record_id: str, file: tuple) -> RecordAttachment:
        return self._client.create(custom_object_key=custom_object_key, record_id=record_id, file=file)

    def update(self, custom_object_key: str, record_id: str, attachment_id: str, **kwargs) -> RecordAttachment:
        return self._client.update(
            custom_object_key=custom_object_key, record_id=record_id, attachment_id=attachment_id, payload=kwargs
        )

    def delete(self, custom_object_key: str, record_id: str, attachment_id: str) -> None:
        self._client.delete(custom_object_key=custom_object_key, record_id=record_id, attachment_id=attachment_id)

    def download_url(self, custom_object_key: str, record_id: str, attachment_id: str) -> str:
        return self._client.download_url(
            custom_object_key=custom_object_key, record_id=record_id, attachment_id=attachment_id
        )
