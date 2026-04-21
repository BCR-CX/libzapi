from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.workspace_cmds import (
    CreateWorkspaceCmd,
    UpdateWorkspaceCmd,
)
from libzapi.domain.models.ticketing.workspace import Workspace
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.workspace_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class WorkspaceApiClient:
    """HTTP adapter for Zendesk Workspaces with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Workspace]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/workspaces",
            base_url=self._http.base_url,
            items_key="workspaces",
        ):
            yield to_domain(data=obj, cls=Workspace)

    def get(self, workspace_id: int) -> Workspace:
        data = self._http.get(f"/api/v2/workspaces/{int(workspace_id)}")
        return to_domain(data=data["workspace"], cls=Workspace)

    def create(self, entity: CreateWorkspaceCmd) -> Workspace:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/workspaces", payload)
        return to_domain(data=data["workspace"], cls=Workspace)

    def update(self, workspace_id: int, entity: UpdateWorkspaceCmd) -> Workspace:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/workspaces/{int(workspace_id)}", payload
        )
        return to_domain(data=data["workspace"], cls=Workspace)

    def delete(self, workspace_id: int) -> None:
        self._http.delete(f"/api/v2/workspaces/{int(workspace_id)}")

    def destroy_many(self, workspace_ids: Iterable[int]) -> None:
        ids_str = ",".join(str(int(i)) for i in workspace_ids)
        self._http.delete(f"/api/v2/workspaces/destroy_many?ids={ids_str}")

    def reorder(self, workspace_ids: Iterable[int]) -> None:
        payload = {"ids": [int(i) for i in workspace_ids]}
        self._http.put("/api/v2/workspaces/reorder", payload)
