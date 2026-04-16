from __future__ import annotations

from libzapi.infrastructure.api_clients.conversations.integration_api_key_api_client import IntegrationApiKeyApiClient


class IntegrationApiKeysService:
    """High-level service for Sunshine Conversations Integration API Keys."""

    def __init__(self, client: IntegrationApiKeyApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self, integration_id: str):
        return self._client.list_all(self._app_id, integration_id)

    def get(self, integration_id: str, key_id: str):
        return self._client.get(self._app_id, integration_id, key_id)

    def create(self, integration_id: str, display_name: str):
        return self._client.create(self._app_id, integration_id, display_name=display_name)

    def delete(self, integration_id: str, key_id: str) -> None:
        self._client.delete(self._app_id, integration_id, key_id)
