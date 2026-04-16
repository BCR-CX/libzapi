from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.ivr_cmds import CreateIvrMenuCmd, UpdateIvrMenuCmd
from libzapi.domain.models.voice.ivr import IvrMenu
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.ivr_mapper import (
    to_payload_create_menu,
    to_payload_update_menu,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/ivr"


class IvrMenuApiClient:
    """HTTP adapter for Zendesk Voice IVR Menus"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, ivr_id: int) -> Iterator[IvrMenu]:
        data = self._http.get(f"{_BASE}/{int(ivr_id)}/menus")
        items = data.get("menus") or data.get("ivr_menus") or []
        for obj in items:
            yield to_domain(data=obj, cls=IvrMenu)

    def get(self, ivr_id: int, menu_id: int) -> IvrMenu:
        data = self._http.get(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}")
        return to_domain(data=data["menu"], cls=IvrMenu)

    def create(self, ivr_id: int, cmd: CreateIvrMenuCmd) -> IvrMenu:
        payload = to_payload_create_menu(cmd)
        data = self._http.post(f"{_BASE}/{int(ivr_id)}/menus", json=payload)
        return to_domain(data=data["menu"], cls=IvrMenu)

    def update(self, ivr_id: int, menu_id: int, cmd: UpdateIvrMenuCmd) -> IvrMenu:
        payload = to_payload_update_menu(cmd)
        data = self._http.put(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}", json=payload)
        return to_domain(data=data["menu"], cls=IvrMenu)

    def delete(self, ivr_id: int, menu_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}")
