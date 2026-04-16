from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.ivr_cmds import CreateIvrMenuCmd, UpdateIvrMenuCmd
from libzapi.domain.models.voice.ivr import IvrMenu
from libzapi.infrastructure.api_clients.voice.ivr_menu_api_client import IvrMenuApiClient


class IvrMenusService:
    def __init__(self, client: IvrMenuApiClient) -> None:
        self._client = client

    def list_all(self, ivr_id: int) -> Iterator[IvrMenu]:
        return self._client.list_all(ivr_id=ivr_id)

    def get(self, ivr_id: int, menu_id: int) -> IvrMenu:
        return self._client.get(ivr_id=ivr_id, menu_id=menu_id)

    def create(self, ivr_id: int, name: str, **kwargs) -> IvrMenu:
        cmd = CreateIvrMenuCmd(name=name, **kwargs)
        return self._client.create(ivr_id=ivr_id, cmd=cmd)

    def update(self, ivr_id: int, menu_id: int, **kwargs) -> IvrMenu:
        cmd = UpdateIvrMenuCmd(**kwargs)
        return self._client.update(ivr_id=ivr_id, menu_id=menu_id, cmd=cmd)

    def delete(self, ivr_id: int, menu_id: int) -> None:
        self._client.delete(ivr_id=ivr_id, menu_id=menu_id)
