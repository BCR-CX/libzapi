from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.view_cmds import (
    CreateViewCmd,
    UpdateViewCmd,
)
from libzapi.domain.models.ticketing.view import View
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.count_mapper import to_count_snapshot
from libzapi.infrastructure.mappers.ticketing.view_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class ViewApiClient:
    """HTTP adapter for Zendesk Views with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[View]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/views",
            base_url=self._http.base_url,
            items_key="views",
        ):
            yield to_domain(data=obj, cls=View)

    def list_active(self) -> Iterator[View]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/views/active",
            base_url=self._http.base_url,
            items_key="views",
        ):
            yield to_domain(data=obj, cls=View)

    def search(self, query: str) -> Iterator[View]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/views/search?query={query}",
            base_url=self._http.base_url,
            items_key="views",
        ):
            yield to_domain(data=obj, cls=View)

    def count(self) -> CountSnapshot:
        data = self._http.get("/api/v2/views/count")
        return to_count_snapshot(data["count"])

    def count_view(self, view_id: int) -> dict:
        data = self._http.get(f"/api/v2/views/{int(view_id)}/count")
        return data.get("view_count", {})

    def count_many(self, view_ids: Iterable[int]) -> list[dict]:
        ids_str = ",".join(str(int(i)) for i in view_ids)
        data = self._http.get(f"/api/v2/views/count_many?ids={ids_str}")
        return list(data.get("view_counts", []))

    def execute(self, view_id: int) -> dict:
        return self._http.get(f"/api/v2/views/{int(view_id)}/execute")

    def get(self, view_id: int) -> View:
        data = self._http.get(f"/api/v2/views/{int(view_id)}")
        return to_domain(data=data["view"], cls=View)

    def create(self, entity: CreateViewCmd) -> View:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/views", payload)
        return to_domain(data=data["view"], cls=View)

    def update(self, view_id: int, entity: UpdateViewCmd) -> View:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/views/{int(view_id)}", payload)
        return to_domain(data=data["view"], cls=View)

    def delete(self, view_id: int) -> None:
        self._http.delete(f"/api/v2/views/{int(view_id)}")

    def update_many(
        self, updates: Iterable[tuple[int, UpdateViewCmd]]
    ) -> JobStatus:
        items = []
        for view_id, cmd in updates:
            item = to_payload_update(cmd)["view"]
            item["id"] = int(view_id)
            items.append(item)
        data = self._http.put(
            "/api/v2/views/update_many", {"views": items}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, view_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in view_ids)
        data = (
            self._http.delete(f"/api/v2/views/destroy_many?ids={ids_str}")
            or {}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)
