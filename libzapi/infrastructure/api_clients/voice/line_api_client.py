from __future__ import annotations

from typing import Iterator

from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items

_BASE = "/api/v2/channels/voice/lines"


class LineApiClient:
    """HTTP adapter for Zendesk Voice Lines"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[dict]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="lines",
        ):
            yield obj
