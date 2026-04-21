from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.workspace_cmds import (
    CreateWorkspaceCmd,
    UpdateWorkspaceCmd,
)
from libzapi.domain.models.ticketing.workspace import Workspace
from libzapi.infrastructure.api_clients.ticketing.workspace_api_client import (
    WorkspaceApiClient,
)


class WorkspaceService:
    """High-level service using the API client."""

    def __init__(self, client: WorkspaceApiClient) -> None:
        self._client = client

    def list(self) -> Iterable[Workspace]:
        return self._client.list()

    def get(self, workspace_id: int) -> Workspace:
        return self._client.get(workspace_id=workspace_id)

    def create(self, **fields) -> Workspace:
        return self._client.create(entity=CreateWorkspaceCmd(**fields))

    def update(self, workspace_id: int, **fields) -> Workspace:
        return self._client.update(
            workspace_id=workspace_id, entity=UpdateWorkspaceCmd(**fields)
        )

    def delete(self, workspace_id: int) -> None:
        self._client.delete(workspace_id=workspace_id)

    def destroy_many(self, workspace_ids: Iterable[int]) -> None:
        self._client.destroy_many(workspace_ids=workspace_ids)

    def reorder(self, workspace_ids: Iterable[int]) -> None:
        self._client.reorder(workspace_ids=workspace_ids)
