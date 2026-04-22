from __future__ import annotations

from typing import Iterator

from libzapi.infrastructure.api_clients.ticketing.search_api_client import (
    SearchApiClient,
)


class SearchService:
    """High-level service for Zendesk unified Search."""

    def __init__(self, client: SearchApiClient) -> None:
        self._client = client

    def search(
        self,
        query: str,
        *,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> Iterator[dict]:
        return self._client.search(
            query=query, sort_by=sort_by, sort_order=sort_order
        )

    def count(self, query: str) -> int:
        return self._client.count(query=query)

    def export(
        self,
        query: str,
        *,
        filter_type: str,
        page_size: int | None = None,
    ) -> Iterator[dict]:
        return self._client.export(
            query=query, filter_type=filter_type, page_size=page_size
        )
