from __future__ import annotations

from urllib.parse import quote

from libzapi.domain.models.ticketing.attachment import Attachment
from libzapi.domain.models.ticketing.upload import Upload
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain


class AttachmentApiClient:
    """HTTP adapter for Zendesk Attachments and Uploads."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, attachment_id: int) -> Attachment:
        data = self._http.get(f"/api/v2/attachments/{int(attachment_id)}")
        return to_domain(data=data["attachment"], cls=Attachment)

    def delete(self, attachment_id: int) -> None:
        self._http.delete(f"/api/v2/attachments/{int(attachment_id)}")

    def redact(self, attachment_id: int) -> Attachment:
        data = self._http.put(
            f"/api/v2/attachments/{int(attachment_id)}/redact", {}
        )
        return to_domain(data=data["attachment"], cls=Attachment)

    def upload(
        self,
        file: tuple,
        filename: str | None = None,
        token: str | None = None,
    ) -> Upload:
        name = filename or file[0]
        path = f"/api/v2/uploads?filename={quote(name)}"
        if token:
            path += f"&token={quote(token)}"
        data = self._http.post_multipart(
            path, files={"uploaded_data": file}
        )
        return to_domain(data=data["upload"], cls=Upload)

    def delete_upload(self, token: str) -> None:
        self._http.delete(f"/api/v2/uploads/{quote(token)}")
