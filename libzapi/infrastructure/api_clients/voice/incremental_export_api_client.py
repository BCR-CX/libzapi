from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.voice.call import Call, CallLeg
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/stats/incremental"


class IncrementalExportApiClient:
    """HTTP adapter for Zendesk Voice Incremental Exports"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def calls(self, start_time: int) -> Iterator[Call]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/calls?start_time={int(start_time)}",
            base_url=self._http.base_url,
            items_key="calls",
        ):
            yield to_domain(data=obj, cls=Call)

    def legs(self, start_time: int) -> Iterator[CallLeg]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/legs?start_time={int(start_time)}",
            base_url=self._http.base_url,
            items_key="legs",
        ):
            yield to_domain(data=obj, cls=CallLeg)
