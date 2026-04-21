from __future__ import annotations

from libzapi.domain.models.ticketing.attachment import Attachment
from libzapi.domain.models.ticketing.upload import Upload
from libzapi.infrastructure.api_clients.ticketing import AttachmentApiClient


class AttachmentsService:
    """High-level service using the API client."""

    def __init__(self, client: AttachmentApiClient) -> None:
        self._client = client

    def get(self, attachment_id: int) -> Attachment:
        return self._client.get(attachment_id=attachment_id)

    def delete(self, attachment_id: int) -> None:
        self._client.delete(attachment_id=attachment_id)

    def redact(self, attachment_id: int) -> Attachment:
        return self._client.redact(attachment_id=attachment_id)

    def upload(
        self,
        file: tuple,
        filename: str | None = None,
        token: str | None = None,
    ) -> Upload:
        return self._client.upload(file=file, filename=filename, token=token)

    def delete_upload(self, token: str) -> None:
        self._client.delete_upload(token=token)
