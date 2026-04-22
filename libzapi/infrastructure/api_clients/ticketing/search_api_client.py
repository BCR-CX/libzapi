from __future__ import annotations

from typing import Iterator
from urllib.parse import urlencode

from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items


def _qs(query: str, **extra: str | None) -> str:
    params: dict[str, str] = {"query": query}
    params.update({k: v for k, v in extra.items() if v is not None})
    return urlencode(params)


class SearchApiClient:
    """HTTP adapter for Zendesk unified Search (ticket/user/org/group)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def search(
        self,
        query: str,
        *,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> Iterator[dict]:
        qs = _qs(query, sort_by=sort_by, sort_order=sort_order)
        yield from yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/search?{qs}",
            base_url=self._http.base_url,
            items_key="results",
        )

    def count(self, query: str) -> int:
        data = self._http.get(f"/api/v2/search/count?{_qs(query)}")
        return int(data.get("count", 0))

    def export(
        self,
        query: str,
        *,
        filter_type: str,
        page_size: int | None = None,
    ) -> Iterator[dict]:
        qs = _qs(
            query,
            **{
                "filter[type]": filter_type,
                "page[size]": str(page_size) if page_size else None,
            },
        )
        yield from yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/search/export?{qs}",
            base_url=self._http.base_url,
            items_key="results",
        )
