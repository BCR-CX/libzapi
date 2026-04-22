from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.bookmark_cmds import CreateBookmarkCmd
from libzapi.domain.models.ticketing.bookmark import Bookmark
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.bookmark_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class BookmarkApiClient:
    """HTTP adapter for Zendesk Bookmarks (current user's bookmarks)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Bookmark]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/bookmarks",
            base_url=self._http.base_url,
            items_key="bookmarks",
        ):
            yield to_domain(data=obj, cls=Bookmark)

    def create(self, entity: CreateBookmarkCmd) -> Bookmark:
        data = self._http.post("/api/v2/bookmarks", to_payload_create(entity))
        return to_domain(data=data["bookmark"], cls=Bookmark)

    def delete(self, bookmark_id: int) -> None:
        self._http.delete(f"/api/v2/bookmarks/{int(bookmark_id)}")
