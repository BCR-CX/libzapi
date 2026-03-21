from typing import Iterable
from libzapi.application.commands.help_center.permission_group_cmds import (
    CreatePermissionGroupCmd,
    UpdatePermissionGroupCmd,
)
from libzapi.domain.models.help_center.management_permission_group import PermissionGroup
from libzapi.infrastructure.api_clients.help_center.permission_group_api_client import PermissionGroupApiClient


class PermissionGroupsService:
    def __init__(self, client: PermissionGroupApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[PermissionGroup]:
        return self._client.list_all()

    def get(self, permission_group_id: int) -> PermissionGroup:
        return self._client.get(permission_group_id=permission_group_id)

    def create(self, name: str, edit=None, publish=None) -> PermissionGroup:
        cmd = CreatePermissionGroupCmd(name=name, edit=edit, publish=publish)
        return self._client.create(cmd=cmd)

    def update(self, permission_group_id: int, name=None, edit=None, publish=None) -> PermissionGroup:
        cmd = UpdatePermissionGroupCmd(name=name, edit=edit, publish=publish)
        return self._client.update(permission_group_id=permission_group_id, cmd=cmd)

    def delete(self, permission_group_id: int) -> None:
        self._client.delete(permission_group_id=permission_group_id)
