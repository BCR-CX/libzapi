from __future__ import annotations

from libzapi.infrastructure.api_clients.conversations.device_api_client import DeviceApiClient


class DevicesService:
    """High-level service for Sunshine Conversations Devices."""

    def __init__(self, client: DeviceApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self, user_id: str):
        return self._client.list_all(self._app_id, user_id)

    def get(self, user_id: str, device_id: str):
        return self._client.get(self._app_id, user_id, device_id)
