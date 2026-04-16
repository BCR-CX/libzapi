from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.ivr_cmds import CreateIvrRouteCmd, UpdateIvrRouteCmd
from libzapi.domain.models.voice.ivr import IvrRoute
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.ivr_mapper import (
    to_payload_create_route,
    to_payload_update_route,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/ivr"


class IvrRouteApiClient:
    """HTTP adapter for Zendesk Voice IVR Routes"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, ivr_id: int, menu_id: int) -> Iterator[IvrRoute]:
        data = self._http.get(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}/routes")
        items = data.get("routes") or data.get("ivr_routes") or []
        for obj in items:
            yield to_domain(data=obj, cls=IvrRoute)

    def get(self, ivr_id: int, menu_id: int, route_id: int) -> IvrRoute:
        data = self._http.get(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}/routes/{int(route_id)}")
        return to_domain(data=data["route"], cls=IvrRoute)

    def create(self, ivr_id: int, menu_id: int, cmd: CreateIvrRouteCmd) -> IvrRoute:
        payload = to_payload_create_route(cmd)
        data = self._http.post(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}/routes", json=payload)
        return to_domain(data=data["route"], cls=IvrRoute)

    def update(self, ivr_id: int, menu_id: int, route_id: int, cmd: UpdateIvrRouteCmd) -> IvrRoute:
        payload = to_payload_update_route(cmd)
        data = self._http.put(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}/routes/{int(route_id)}", json=payload)
        return to_domain(data=data["route"], cls=IvrRoute)

    def delete(self, ivr_id: int, menu_id: int, route_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(ivr_id)}/menus/{int(menu_id)}/routes/{int(route_id)}")
