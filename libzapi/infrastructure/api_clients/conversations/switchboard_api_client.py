from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.switchboard_cmds import CreateSwitchboardCmd, UpdateSwitchboardCmd
from libzapi.domain.models.conversations.switchboard import Switchboard
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.conversations.switchboard_mapper import (
    to_payload_create_switchboard,
    to_payload_update_switchboard,
)
from libzapi.infrastructure.serialization.parse import to_domain


class SwitchboardApiClient:
    """HTTP adapter for Sunshine Conversations Switchboards."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str) -> Iterator[Switchboard]:
        data = self._http.get(f"/v2/apps/{app_id}/switchboards")
        for obj in data.get("switchboards", []):
            yield to_domain(data=obj, cls=Switchboard)

    def create(self, app_id: str, cmd: CreateSwitchboardCmd) -> Switchboard:
        payload = to_payload_create_switchboard(cmd)
        data = self._http.post(f"/v2/apps/{app_id}/switchboards", payload)
        return to_domain(data=data["switchboard"], cls=Switchboard)

    def update(self, app_id: str, switchboard_id: str, cmd: UpdateSwitchboardCmd) -> Switchboard:
        payload = to_payload_update_switchboard(cmd)
        data = self._http.patch(f"/v2/apps/{app_id}/switchboards/{switchboard_id}", payload)
        return to_domain(data=data["switchboard"], cls=Switchboard)

    def delete(self, app_id: str, switchboard_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/switchboards/{switchboard_id}")
