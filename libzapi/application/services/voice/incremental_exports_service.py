from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.voice.call import Call, CallLeg
from libzapi.infrastructure.api_clients.voice.incremental_export_api_client import IncrementalExportApiClient


class IncrementalExportsService:
    def __init__(self, client: IncrementalExportApiClient) -> None:
        self._client = client

    def calls(self, start_time: int) -> Iterator[Call]:
        return self._client.calls(start_time=start_time)

    def legs(self, start_time: int) -> Iterator[CallLeg]:
        return self._client.legs(start_time=start_time)
