from __future__ import annotations

from libzapi.application.commands.conversations.switchboard_cmds import CreateSwitchboardCmd, UpdateSwitchboardCmd
from libzapi.infrastructure.api_clients.conversations.switchboard_api_client import SwitchboardApiClient


class SwitchboardsService:
    """High-level service for Sunshine Conversations Switchboards."""

    def __init__(self, client: SwitchboardApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self):
        return self._client.list_all(self._app_id)

    def create(self, **kwargs):
        cmd = CreateSwitchboardCmd(**kwargs)
        return self._client.create(self._app_id, cmd)

    def update(self, switchboard_id: str, **kwargs):
        cmd = UpdateSwitchboardCmd(**kwargs)
        return self._client.update(self._app_id, switchboard_id, cmd)

    def delete(self, switchboard_id: str) -> None:
        self._client.delete(self._app_id, switchboard_id)
