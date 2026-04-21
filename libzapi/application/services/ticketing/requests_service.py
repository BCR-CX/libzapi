from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.request_cmds import (
    CreateRequestCmd,
    UpdateRequestCmd,
)
from libzapi.domain.models.ticketing.request import Request
from libzapi.infrastructure.api_clients.ticketing.request_api_client import (
    RequestApiClient,
)


class RequestsService:
    """High-level service using the API client."""

    def __init__(self, client: RequestApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Request]:
        return self._client.list()

    def list_by_user(self, user_id: int) -> Iterable[Request]:
        return self._client.list_user(user_id)

    def search(self, query: str) -> Iterable[Request]:
        return self._client.search(query)

    def get_by_id(self, request_id: int) -> Request:
        return self._client.get(request_id)

    def create(self, **fields) -> Request:
        return self._client.create(entity=CreateRequestCmd(**fields))

    def update(self, request_id: int, **fields) -> Request:
        return self._client.update(
            request_id=request_id, entity=UpdateRequestCmd(**fields)
        )

    def list_comments(self, request_id: int) -> Iterator[dict]:
        return self._client.list_comments(request_id)

    def get_comment(self, request_id: int, comment_id: int) -> dict:
        return self._client.get_comment(
            request_id=request_id, comment_id=comment_id
        )
