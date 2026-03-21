from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.permission_group_cmds import (
    CreatePermissionGroupCmd,
    UpdatePermissionGroupCmd,
)
from libzapi.domain.models.help_center.management_permission_group import PermissionGroup
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.permission_group_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class PermissionGroupApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[PermissionGroup]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/guide/permission_groups",
            base_url=self._http.base_url,
            items_key="permission_groups",
        ):
            yield to_domain(data=obj, cls=PermissionGroup)

    def get(self, permission_group_id: int) -> PermissionGroup:
        data = self._http.get(f"/api/v2/guide/permission_groups/{int(permission_group_id)}")
        return to_domain(data=data["permission_group"], cls=PermissionGroup)

    def create(self, cmd: CreatePermissionGroupCmd) -> PermissionGroup:
        payload = to_payload_create(cmd)
        data = self._http.post("/api/v2/guide/permission_groups", json=payload)
        return to_domain(data=data["permission_group"], cls=PermissionGroup)

    def update(self, permission_group_id: int, cmd: UpdatePermissionGroupCmd) -> PermissionGroup:
        payload = to_payload_update(cmd)
        data = self._http.put(f"/api/v2/guide/permission_groups/{int(permission_group_id)}", json=payload)
        return to_domain(data=data["permission_group"], cls=PermissionGroup)

    def delete(self, permission_group_id: int) -> None:
        self._http.delete(f"/api/v2/guide/permission_groups/{int(permission_group_id)}")
