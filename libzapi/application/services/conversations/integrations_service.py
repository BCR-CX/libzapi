from __future__ import annotations

from libzapi.application.commands.conversations.integration_cmds import CreateIntegrationCmd, UpdateIntegrationCmd
from libzapi.infrastructure.api_clients.conversations.integration_api_client import IntegrationApiClient


class IntegrationsService:
    """High-level service for Sunshine Conversations Integrations."""

    def __init__(self, client: IntegrationApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self):
        return self._client.list_all(self._app_id)

    def get(self, integration_id: str):
        return self._client.get(self._app_id, integration_id)

    def create(self, type: str, **kwargs):
        cmd = CreateIntegrationCmd(type=type, **kwargs)
        return self._client.create(self._app_id, cmd)

    def update(self, integration_id: str, **kwargs):
        cmd = UpdateIntegrationCmd(**kwargs)
        return self._client.update(self._app_id, integration_id, cmd)

    def delete(self, integration_id: str) -> None:
        self._client.delete(self._app_id, integration_id)
