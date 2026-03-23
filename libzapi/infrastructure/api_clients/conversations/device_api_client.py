from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.conversations.device import Device
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain


class DeviceApiClient:
    """HTTP adapter for Sunshine Conversations Devices."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str, user_id_or_external_id: str) -> Iterator[Device]:
        data = self._http.get(f"/v2/apps/{app_id}/users/{user_id_or_external_id}/devices")
        for obj in data.get("devices", []):
            yield to_domain(data=obj, cls=Device)

    def get(self, app_id: str, user_id_or_external_id: str, device_id: str) -> Device:
        data = self._http.get(f"/v2/apps/{app_id}/users/{user_id_or_external_id}/devices/{device_id}")
        return to_domain(data=data["device"], cls=Device)
