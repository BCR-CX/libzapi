from __future__ import annotations

from libzapi.application.commands.conversations.app_cmds import CreateAppCmd, UpdateAppCmd
from libzapi.infrastructure.api_clients.conversations.app_api_client import AppApiClient


class AppsService:
    """High-level service for Sunshine Conversations Apps."""

    def __init__(self, client: AppApiClient) -> None:
        self._client = client

    def list_all(self):
        return self._client.list_all()

    def get(self, app_id: str):
        return self._client.get(app_id)

    def create(self, display_name: str, **kwargs):
        cmd = CreateAppCmd(displayName=display_name, **kwargs)
        return self._client.create(cmd)

    def update(self, app_id: str, **kwargs):
        cmd = UpdateAppCmd(**kwargs)
        return self._client.update(app_id, cmd)

    def delete(self, app_id: str) -> None:
        self._client.delete(app_id)
