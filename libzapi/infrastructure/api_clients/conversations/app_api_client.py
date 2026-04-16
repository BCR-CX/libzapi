from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.app_cmds import CreateAppCmd, UpdateAppCmd
from libzapi.domain.models.conversations.app import App
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.mappers.conversations.app_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class AppApiClient:
    """HTTP adapter for Sunshine Conversations Apps."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[App]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path="/v2/apps",
            items_key="apps",
        ):
            yield to_domain(data=obj, cls=App)

    def get(self, app_id: str) -> App:
        data = self._http.get(f"/v2/apps/{app_id}")
        return to_domain(data=data["app"], cls=App)

    def create(self, cmd: CreateAppCmd) -> App:
        payload = to_payload_create(cmd)
        data = self._http.post("/v2/apps", payload)
        return to_domain(data=data["app"], cls=App)

    def update(self, app_id: str, cmd: UpdateAppCmd) -> App:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"/v2/apps/{app_id}", payload)
        return to_domain(data=data["app"], cls=App)

    def delete(self, app_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}")
