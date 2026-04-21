from __future__ import annotations

from typing import Any, Iterable

from libzapi.application.commands.ticketing.view_cmds import (
    CreateViewCmd,
    UpdateViewCmd,
)
from libzapi.domain.models.ticketing.view import View
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing.view_api_client import ViewApiClient


class ViewsService:
    """High-level service using the API client."""

    def __init__(self, client: ViewApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[View]:
        return self._client.list_all()

    def list_active(self) -> Iterable[View]:
        return self._client.list_active()

    def search(self, query: str) -> Iterable[View]:
        return self._client.search(query=query)

    def count(self) -> CountSnapshot:
        return self._client.count()

    def count_view(self, view_id: int) -> dict:
        return self._client.count_view(view_id=view_id)

    def count_many(self, view_ids: Iterable[int]) -> list[dict]:
        return self._client.count_many(view_ids=view_ids)

    def execute(self, view_id: int) -> dict:
        return self._client.execute(view_id=view_id)

    def get_by_id(self, view_id: int) -> View:
        return self._client.get(view_id=view_id)

    def create(self, **fields) -> View:
        return self._client.create(entity=CreateViewCmd(**fields))

    def update(self, view_id: int, **fields) -> View:
        return self._client.update(
            view_id=view_id, entity=UpdateViewCmd(**fields)
        )

    def delete(self, view_id: int) -> None:
        self._client.delete(view_id=view_id)

    def update_many(
        self, updates: Iterable[tuple[int, dict[str, Any]]]
    ) -> JobStatus:
        pairs = [
            (view_id, UpdateViewCmd(**fields))
            for view_id, fields in updates
        ]
        return self._client.update_many(updates=pairs)

    def destroy_many(self, view_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(view_ids=view_ids)
