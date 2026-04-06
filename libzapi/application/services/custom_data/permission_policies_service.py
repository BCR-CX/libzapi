from typing import Iterator

from libzapi.application.commands.custom_data.permission_cmds import UpdatePermissionPolicyCmd
from libzapi.domain.models.custom_data.permission_policy import PermissionPolicy
from libzapi.infrastructure.api_clients.custom_data import PermissionPolicyApiClient


class PermissionPoliciesService:
    def __init__(self, client: PermissionPolicyApiClient) -> None:
        self._client = client

    def list_all(self, custom_object_key: str) -> Iterator[PermissionPolicy]:
        return self._client.list_all(custom_object_key=custom_object_key)

    def get(self, custom_object_key: str, policy_id: str) -> PermissionPolicy:
        return self._client.get(custom_object_key=custom_object_key, policy_id=policy_id)

    def update(self, custom_object_key: str, policy_id: str, **kwargs) -> PermissionPolicy:
        cmd = UpdatePermissionPolicyCmd(**kwargs)
        return self._client.update(custom_object_key=custom_object_key, policy_id=policy_id, cmd=cmd)
