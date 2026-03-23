from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.integration_cmds import CreateIntegrationCmd, UpdateIntegrationCmd
from libzapi.domain.models.conversations.integration import Integration
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.mappers.conversations.integration_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class IntegrationApiClient:
    """HTTP adapter for Sunshine Conversations Integrations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str) -> Iterator[Integration]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/integrations",
            items_key="integrations",
        ):
            yield to_domain(data=obj, cls=Integration)

    def get(self, app_id: str, integration_id: str) -> Integration:
        data = self._http.get(f"/v2/apps/{app_id}/integrations/{integration_id}")
        return to_domain(data=data["integration"], cls=Integration)

    def create(self, app_id: str, cmd: CreateIntegrationCmd) -> Integration:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/v2/apps/{app_id}/integrations", payload)
        return to_domain(data=data["integration"], cls=Integration)

    def update(self, app_id: str, integration_id: str, cmd: UpdateIntegrationCmd) -> Integration:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"/v2/apps/{app_id}/integrations/{integration_id}", payload)
        return to_domain(data=data["integration"], cls=Integration)

    def delete(self, app_id: str, integration_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/integrations/{integration_id}")
