from __future__ import annotations

from libzapi.application.commands.voice.digital_line_cmds import (
    CreateDigitalLineCmd,
    UpdateDigitalLineCmd,
)
from libzapi.domain.models.voice.digital_line import DigitalLine
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.digital_line_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/digital_lines"


class DigitalLineApiClient:
    """HTTP adapter for Zendesk Voice Digital Lines"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, digital_line_id: int) -> DigitalLine:
        data = self._http.get(f"{_BASE}/{int(digital_line_id)}")
        return to_domain(data=data["digital_line"], cls=DigitalLine)

    def create(self, cmd: CreateDigitalLineCmd) -> DigitalLine:
        payload = to_payload_create(cmd)
        data = self._http.post(_BASE, json=payload)
        return to_domain(data=data["digital_line"], cls=DigitalLine)

    def update(self, digital_line_id: int, cmd: UpdateDigitalLineCmd) -> DigitalLine:
        payload = to_payload_update(cmd)
        data = self._http.put(f"{_BASE}/{int(digital_line_id)}", json=payload)
        return to_domain(data=data["digital_line"], cls=DigitalLine)

    def delete(self, digital_line_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(digital_line_id)}")
