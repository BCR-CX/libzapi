from typing import Iterator

from libzapi.application.commands.custom_data.permission_cmds import CreateAccessRuleCmd, UpdateAccessRuleCmd
from libzapi.domain.models.custom_data.access_rule import AccessRule
from libzapi.infrastructure.api_clients.custom_data import AccessRuleApiClient


class AccessRulesService:
    def __init__(self, client: AccessRuleApiClient) -> None:
        self._client = client

    def list_all(self, custom_object_key: str) -> Iterator[AccessRule]:
        return self._client.list_all(custom_object_key=custom_object_key)

    def get(self, custom_object_key: str, rule_id: str) -> AccessRule:
        return self._client.get(custom_object_key=custom_object_key, rule_id=rule_id)

    def create(self, custom_object_key: str, name: str, conditions: dict | None = None) -> AccessRule:
        cmd = CreateAccessRuleCmd(name=name, conditions=conditions or {})
        return self._client.create(custom_object_key=custom_object_key, cmd=cmd)

    def update(self, custom_object_key: str, rule_id: str, **kwargs) -> AccessRule:
        cmd = UpdateAccessRuleCmd(**kwargs)
        return self._client.update(custom_object_key=custom_object_key, rule_id=rule_id, cmd=cmd)

    def delete(self, custom_object_key: str, rule_id: str) -> None:
        self._client.delete(custom_object_key=custom_object_key, rule_id=rule_id)

    def definitions(self, custom_object_key: str) -> dict:
        return self._client.definitions(custom_object_key=custom_object_key)
