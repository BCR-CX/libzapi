from __future__ import annotations

from libzapi.infrastructure.api_clients.conversations.app_key_api_client import AppKeyApiClient


class AppKeysService:
    """High-level service for Sunshine Conversations App Keys."""

    def __init__(self, client: AppKeyApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self):
        return self._client.list_all(self._app_id)

    def get(self, key_id: str):
        return self._client.get(self._app_id, key_id)

    def create(self, display_name: str):
        return self._client.create(self._app_id, display_name=display_name)

    def delete(self, key_id: str) -> None:
        self._client.delete(self._app_id, key_id)
