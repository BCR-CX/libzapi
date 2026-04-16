from typing import Iterator

from libzapi.application.commands.custom_data.permission_cmds import CreateAccessRuleCmd, UpdateAccessRuleCmd
from libzapi.domain.models.custom_data.access_rule import AccessRule
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.custom_data.access_rule_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/custom_objects"


class AccessRuleApiClient:
    """HTTP adapter for Zendesk Custom Object Access Rules."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, custom_object_key: str) -> Iterator[AccessRule]:
        data = self._http.get(f"{_BASE}/{custom_object_key}/access_rules")
        for obj in data.get("access_rules", []):
            yield to_domain(data=obj, cls=AccessRule)

    def get(self, custom_object_key: str, rule_id: str) -> AccessRule:
        data = self._http.get(f"{_BASE}/{custom_object_key}/access_rules/{rule_id}")
        return to_domain(data=data["access_rule"], cls=AccessRule)

    def create(self, custom_object_key: str, cmd: CreateAccessRuleCmd) -> AccessRule:
        payload = to_payload_create(cmd)
        data = self._http.post(f"{_BASE}/{custom_object_key}/access_rules", json=payload)
        return to_domain(data=data["access_rule"], cls=AccessRule)

    def update(self, custom_object_key: str, rule_id: str, cmd: UpdateAccessRuleCmd) -> AccessRule:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"{_BASE}/{custom_object_key}/access_rules/{rule_id}", json=payload)
        return to_domain(data=data["access_rule"], cls=AccessRule)

    def delete(self, custom_object_key: str, rule_id: str) -> None:
        self._http.delete(f"{_BASE}/{custom_object_key}/access_rules/{rule_id}")

    def definitions(self, custom_object_key: str) -> dict:
        return self._http.get(f"{_BASE}/{custom_object_key}/access_rules/definitions")
