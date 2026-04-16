from typing import Iterator

from libzapi.application.commands.custom_data.permission_cmds import UpdatePermissionPolicyCmd
from libzapi.domain.models.custom_data.permission_policy import PermissionPolicy
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.custom_data.permission_policy_mapper import to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/custom_objects"


class PermissionPolicyApiClient:
    """HTTP adapter for Zendesk Custom Object Permission Policies."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, custom_object_key: str) -> Iterator[PermissionPolicy]:
        data = self._http.get(f"{_BASE}/{custom_object_key}/permission_policies")
        for obj in data.get("permission_policies", []):
            yield to_domain(data=obj, cls=PermissionPolicy)

    def get(self, custom_object_key: str, policy_id: str) -> PermissionPolicy:
        data = self._http.get(f"{_BASE}/{custom_object_key}/permission_policies/{policy_id}")
        return to_domain(data=data["permission_policy"], cls=PermissionPolicy)

    def update(self, custom_object_key: str, policy_id: str, cmd: UpdatePermissionPolicyCmd) -> PermissionPolicy:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"{_BASE}/{custom_object_key}/permission_policies/{policy_id}", json=payload)
        return to_domain(data=data["permission_policy"], cls=PermissionPolicy)
