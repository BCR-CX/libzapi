from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.custom_data.record_event import RecordEvent
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/custom_objects"


def _extract_next(data: dict, base_url: str) -> str | None:
    """Extract cursor pagination link from Record Events response.

    This API returns ``links`` as a list (e.g. ``[{"next": "..."}]``)
    instead of the standard dict format, so the generic pagination
    utility cannot be used here.
    """
    links = data.get("links")
    if isinstance(links, list):
        for link in links:
            if isinstance(link, dict) and link.get("next"):
                nxt = link["next"]
                return nxt.replace(base_url, "") if nxt.startswith("https://") else nxt
        return None
    if isinstance(links, dict) and links.get("next"):
        nxt = links["next"]
        return nxt.replace(base_url, "") if nxt.startswith("https://") else nxt
    return None


class RecordEventApiClient:
    """HTTP adapter for Zendesk Custom Object Record Events."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, custom_object_key: str, record_id: str, page_size: int = 100) -> Iterator[RecordEvent]:
        path: str | None = f"{_BASE}/{custom_object_key}/records/{record_id}/events?page[size]={page_size}"
        while path:
            data = self._http.get(path)
            for obj in data.get("events", []):
                yield to_domain(data=obj, cls=RecordEvent)
            meta = data.get("meta") or {}
            if not meta.get("has_more"):
                break
            path = _extract_next(data, self._http.base_url)
