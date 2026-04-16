from __future__ import annotations

from typing import Iterator

from libzapi.infrastructure.api_clients.voice.line_api_client import LineApiClient


class LinesService:
    def __init__(self, client: LineApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[dict]:
        return self._client.list_all()
