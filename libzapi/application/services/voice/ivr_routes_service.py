from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.ivr_cmds import CreateIvrRouteCmd, UpdateIvrRouteCmd
from libzapi.domain.models.voice.ivr import IvrRoute
from libzapi.infrastructure.api_clients.voice.ivr_route_api_client import IvrRouteApiClient


class IvrRoutesService:
    def __init__(self, client: IvrRouteApiClient) -> None:
        self._client = client

    def list_all(self, ivr_id: int, menu_id: int) -> Iterator[IvrRoute]:
        return self._client.list_all(ivr_id=ivr_id, menu_id=menu_id)

    def get(self, ivr_id: int, menu_id: int, route_id: int) -> IvrRoute:
        return self._client.get(ivr_id=ivr_id, menu_id=menu_id, route_id=route_id)

    def create(self, ivr_id: int, menu_id: int, action: str, keypress: str, **kwargs) -> IvrRoute:
        cmd = CreateIvrRouteCmd(action=action, keypress=keypress, **kwargs)
        return self._client.create(ivr_id=ivr_id, menu_id=menu_id, cmd=cmd)

    def update(self, ivr_id: int, menu_id: int, route_id: int, **kwargs) -> IvrRoute:
        cmd = UpdateIvrRouteCmd(**kwargs)
        return self._client.update(ivr_id=ivr_id, menu_id=menu_id, route_id=route_id, cmd=cmd)

    def delete(self, ivr_id: int, menu_id: int, route_id: int) -> None:
        self._client.delete(ivr_id=ivr_id, menu_id=menu_id, route_id=route_id)
