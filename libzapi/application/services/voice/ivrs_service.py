from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.ivr_cmds import CreateIvrCmd, UpdateIvrCmd
from libzapi.domain.models.voice.ivr import Ivr
from libzapi.infrastructure.api_clients.voice.ivr_api_client import IvrApiClient


class IvrsService:
    def __init__(self, client: IvrApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[Ivr]:
        return self._client.list_all()

    def get(self, ivr_id: int) -> Ivr:
        return self._client.get(ivr_id=ivr_id)

    def create(self, name: str, phone_number_ids: list[int] | None = None) -> Ivr:
        cmd = CreateIvrCmd(name=name, phone_number_ids=phone_number_ids or [])
        return self._client.create(cmd=cmd)

    def update(self, ivr_id: int, **kwargs) -> Ivr:
        cmd = UpdateIvrCmd(**kwargs)
        return self._client.update(ivr_id=ivr_id, cmd=cmd)

    def delete(self, ivr_id: int) -> None:
        self._client.delete(ivr_id=ivr_id)
