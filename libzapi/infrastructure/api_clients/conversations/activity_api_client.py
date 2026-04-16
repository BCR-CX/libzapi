from __future__ import annotations

from libzapi.infrastructure.http.client import HttpClient


class ActivityApiClient:
    """HTTP adapter for Sunshine Conversations Activity."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def post(self, app_id: str, conversation_id: str, author: dict, type: str) -> dict:
        path = f"/v2/apps/{app_id}/conversations/{conversation_id}/activity"
        return self._http.post(path, {"author": author, "type": type})
