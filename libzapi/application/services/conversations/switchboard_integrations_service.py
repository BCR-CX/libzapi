from __future__ import annotations

from libzapi.application.commands.conversations.switchboard_cmds import (
    CreateSwitchboardIntegrationCmd,
    UpdateSwitchboardIntegrationCmd,
)
from libzapi.infrastructure.api_clients.conversations.switchboard_integration_api_client import (
    SwitchboardIntegrationApiClient,
)


class SwitchboardIntegrationsService:
    """High-level service for Sunshine Conversations Switchboard Integrations."""

    def __init__(self, client: SwitchboardIntegrationApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self, switchboard_id: str):
        return self._client.list_all(self._app_id, switchboard_id)

    def create(self, switchboard_id: str, name: str, integration_id: str, **kwargs):
        cmd = CreateSwitchboardIntegrationCmd(name=name, integrationId=integration_id, **kwargs)
        return self._client.create(self._app_id, switchboard_id, cmd)

    def update(self, switchboard_id: str, switchboard_integration_id: str, **kwargs):
        cmd = UpdateSwitchboardIntegrationCmd(**kwargs)
        return self._client.update(self._app_id, switchboard_id, switchboard_integration_id, cmd)

    def delete(self, switchboard_id: str, switchboard_integration_id: str) -> None:
        self._client.delete(self._app_id, switchboard_id, switchboard_integration_id)
