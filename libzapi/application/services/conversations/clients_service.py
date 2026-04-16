from __future__ import annotations

from libzapi.infrastructure.api_clients.conversations.client_api_client import ClientApiClient


class ClientsService:
    """High-level service for Sunshine Conversations Clients."""

    def __init__(self, client: ClientApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self, user_id: str):
        return self._client.list_all(self._app_id, user_id)

    def create(self, user_id: str, payload: dict):
        return self._client.create(self._app_id, user_id, payload=payload)

    def remove(self, user_id: str, client_id: str) -> None:
        self._client.remove(self._app_id, user_id, client_id)
