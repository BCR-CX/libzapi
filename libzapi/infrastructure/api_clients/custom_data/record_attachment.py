from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.custom_data.record_attachment import RecordAttachment
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/custom_objects"


class RecordAttachmentApiClient:
    """HTTP adapter for Zendesk Custom Object Record Attachments."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def _path(self, key: str, record_id: str) -> str:
        return f"{_BASE}/{key}/records/{record_id}/attachments"

    def list_all(self, custom_object_key: str, record_id: str) -> Iterator[RecordAttachment]:
        data = self._http.get(self._path(custom_object_key, record_id))
        for obj in data.get("attachments", []):
            yield to_domain(data=obj, cls=RecordAttachment)

    def create(self, custom_object_key: str, record_id: str, file: tuple) -> RecordAttachment:
        data = self._http.post_multipart(self._path(custom_object_key, record_id), files={"file": file})
        return to_domain(data=data["attachment"], cls=RecordAttachment)

    def update(self, custom_object_key: str, record_id: str, attachment_id: str, payload: dict) -> RecordAttachment:
        data = self._http.put(f"{self._path(custom_object_key, record_id)}/{attachment_id}", json=payload)
        return to_domain(data=data["attachment"], cls=RecordAttachment)

    def delete(self, custom_object_key: str, record_id: str, attachment_id: str) -> None:
        self._http.delete(f"{self._path(custom_object_key, record_id)}/{attachment_id}")

    def download_url(self, custom_object_key: str, record_id: str, attachment_id: str) -> str:
        return f"{self._http.base_url}{self._path(custom_object_key, record_id)}/{attachment_id}/download"
