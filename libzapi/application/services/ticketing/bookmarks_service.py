from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.bookmark_cmds import CreateBookmarkCmd
from libzapi.domain.models.ticketing.bookmark import Bookmark
from libzapi.infrastructure.api_clients.ticketing.bookmark_api_client import (
    BookmarkApiClient,
)


class BookmarksService:
    def __init__(self, client: BookmarkApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Bookmark]:
        return self._client.list()

    def create(self, ticket_id: int) -> Bookmark:
        return self._client.create(entity=CreateBookmarkCmd(ticket_id=ticket_id))

    def delete(self, bookmark_id: int) -> None:
        self._client.delete(bookmark_id=bookmark_id)
