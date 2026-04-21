from __future__ import annotations

from typing import Iterator
from urllib.parse import quote

from libzapi.application.commands.ticketing.request_cmds import (
    CreateRequestCmd,
    UpdateRequestCmd,
)
from libzapi.domain.models.ticketing.request import Request
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.request_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class RequestApiClient:
    """HTTP adapter for Zendesk Requests."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Request]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/requests",
            base_url=self._http.base_url,
            items_key="requests",
        ):
            yield to_domain(data=obj, cls=Request)

    def list_user(self, user_id: int) -> Iterator[Request]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/users/{int(user_id)}/requests",
            base_url=self._http.base_url,
            items_key="requests",
        ):
            yield to_domain(data=obj, cls=Request)

    def search(self, query: str) -> Iterator[Request]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/requests/search?query={quote(query)}",
            base_url=self._http.base_url,
            items_key="requests",
        ):
            yield to_domain(data=obj, cls=Request)

    def get(self, request_id: int) -> Request:
        data = self._http.get(f"/api/v2/requests/{int(request_id)}")
        return to_domain(data=data["request"], cls=Request)

    def create(self, entity: CreateRequestCmd) -> Request:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/requests", payload)
        return to_domain(data=data["request"], cls=Request)

    def update(self, request_id: int, entity: UpdateRequestCmd) -> Request:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/requests/{int(request_id)}", payload
        )
        return to_domain(data=data["request"], cls=Request)

    def list_comments(self, request_id: int) -> Iterator[dict]:
        yield from yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/requests/{int(request_id)}/comments",
            base_url=self._http.base_url,
            items_key="comments",
        )

    def get_comment(self, request_id: int, comment_id: int) -> dict:
        data = self._http.get(
            f"/api/v2/requests/{int(request_id)}/comments/{int(comment_id)}"
        )
        return data["comment"]
