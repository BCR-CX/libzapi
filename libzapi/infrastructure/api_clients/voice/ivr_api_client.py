from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.ivr_cmds import CreateIvrCmd, UpdateIvrCmd
from libzapi.domain.models.voice.ivr import Ivr
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.ivr_mapper import (
    to_payload_create_ivr,
    to_payload_update_ivr,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/ivr"


class IvrApiClient:
    """HTTP adapter for Zendesk Voice IVR"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Ivr]:
        data = self._http.get(_BASE)
        for obj in data["ivrs"]:
            yield to_domain(data=obj, cls=Ivr)

    def get(self, ivr_id: int) -> Ivr:
        data = self._http.get(f"{_BASE}/{int(ivr_id)}")
        return to_domain(data=data["ivr"], cls=Ivr)

    def create(self, cmd: CreateIvrCmd) -> Ivr:
        payload = to_payload_create_ivr(cmd)
        data = self._http.post(_BASE, json=payload)
        return to_domain(data=data["ivr"], cls=Ivr)

    def update(self, ivr_id: int, cmd: UpdateIvrCmd) -> Ivr:
        payload = to_payload_update_ivr(cmd)
        data = self._http.put(f"{_BASE}/{int(ivr_id)}", json=payload)
        return to_domain(data=data["ivr"], cls=Ivr)

    def delete(self, ivr_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(ivr_id)}")
