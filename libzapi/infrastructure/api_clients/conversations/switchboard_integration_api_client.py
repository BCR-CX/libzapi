from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.switchboard_cmds import (
    CreateSwitchboardIntegrationCmd,
    UpdateSwitchboardIntegrationCmd,
)
from libzapi.domain.models.conversations.switchboard import SwitchboardIntegration
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.mappers.conversations.switchboard_mapper import (
    to_payload_create_switchboard_integration,
    to_payload_update_switchboard_integration,
)
from libzapi.infrastructure.serialization.parse import to_domain


class SwitchboardIntegrationApiClient:
    """HTTP adapter for Sunshine Conversations Switchboard Integrations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str, switchboard_id: str) -> Iterator[SwitchboardIntegration]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/switchboards/{switchboard_id}/switchboardIntegrations",
            items_key="switchboardIntegrations",
        ):
            yield to_domain(data=obj, cls=SwitchboardIntegration)

    def create(self, app_id: str, switchboard_id: str, cmd: CreateSwitchboardIntegrationCmd) -> SwitchboardIntegration:
        payload = to_payload_create_switchboard_integration(cmd)
        data = self._http.post(
            f"/v2/apps/{app_id}/switchboards/{switchboard_id}/switchboardIntegrations",
            payload,
        )
        return to_domain(data=data["switchboardIntegration"], cls=SwitchboardIntegration)

    def update(
        self,
        app_id: str,
        switchboard_id: str,
        switchboard_integration_id: str,
        cmd: UpdateSwitchboardIntegrationCmd,
    ) -> SwitchboardIntegration:
        payload = to_payload_update_switchboard_integration(cmd)
        data = self._http.patch(
            f"/v2/apps/{app_id}/switchboards/{switchboard_id}/switchboardIntegrations/{switchboard_integration_id}",
            payload,
        )
        return to_domain(data=data["switchboardIntegration"], cls=SwitchboardIntegration)

    def delete(self, app_id: str, switchboard_id: str, switchboard_integration_id: str) -> None:
        self._http.delete(
            f"/v2/apps/{app_id}/switchboards/{switchboard_id}/switchboardIntegrations/{switchboard_integration_id}"
        )
