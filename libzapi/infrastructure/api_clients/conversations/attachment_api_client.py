from __future__ import annotations

from libzapi.domain.models.conversations.attachment import Attachment
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain


class AttachmentApiClient:
    """HTTP adapter for Sunshine Conversations Attachments."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def upload(self, app_id: str, file: tuple) -> Attachment:
        data = self._http.post_multipart(f"/v2/apps/{app_id}/attachments", files={"source": file})
        return to_domain(data=data["attachment"], cls=Attachment)

    def delete(self, app_id: str, media_url: str) -> dict:
        return self._http.post(f"/v2/apps/{app_id}/attachments/remove", {"mediaUrl": media_url})
