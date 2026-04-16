from __future__ import annotations

from libzapi.infrastructure.api_clients.conversations.activity_api_client import ActivityApiClient


class ActivitiesService:
    """High-level service for Sunshine Conversations Activities."""

    def __init__(self, client: ActivityApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def post(self, conversation_id: str, author: dict, type: str):
        return self._client.post(self._app_id, conversation_id, author=author, type=type)
