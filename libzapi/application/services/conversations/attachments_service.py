from __future__ import annotations

from libzapi.infrastructure.api_clients.conversations.attachment_api_client import AttachmentApiClient


class AttachmentsService:
    """High-level service for Sunshine Conversations Attachments."""

    def __init__(self, client: AttachmentApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def upload(self, file):
        return self._client.upload(self._app_id, file)

    def delete(self, media_url: str) -> None:
        self._client.delete(self._app_id, media_url)
