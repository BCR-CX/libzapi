from __future__ import annotations

from libzapi.application.commands.voice.digital_line_cmds import CreateDigitalLineCmd, UpdateDigitalLineCmd
from libzapi.domain.models.voice.digital_line import DigitalLine
from libzapi.infrastructure.api_clients.voice.digital_line_api_client import DigitalLineApiClient


class DigitalLinesService:
    def __init__(self, client: DigitalLineApiClient) -> None:
        self._client = client

    def get(self, digital_line_id: int) -> DigitalLine:
        return self._client.get(digital_line_id=digital_line_id)

    def create(self, **kwargs) -> DigitalLine:
        cmd = CreateDigitalLineCmd(**kwargs)
        return self._client.create(cmd=cmd)

    def update(self, digital_line_id: int, **kwargs) -> DigitalLine:
        cmd = UpdateDigitalLineCmd(**kwargs)
        return self._client.update(digital_line_id=digital_line_id, cmd=cmd)

    def delete(self, digital_line_id: int) -> None:
        self._client.delete(digital_line_id=digital_line_id)
