from __future__ import annotations
from typing import Iterable

from libzapi.application.commands.agent_availability.capacity_rule_cmds import (
    CreateCapacityRuleCmd,
    UpdateCapacityRuleCmd,
)
from libzapi.domain.models.agent_availability.capacity_rule import CapacityRule
from libzapi.domain.models.agent_availability.capacity_rule_assignee import CapacityRuleAssignee
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.agent_availability.capacity_rule_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/capacity/rules"


class CapacityRuleApiClient:
    """HTTP adapter for Zendesk Capacity Rules."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterable[CapacityRule]:
        data = self._http.get(_BASE)
        items = data if isinstance(data, list) else data.get("data", [])
        for obj in items:
            yield to_domain(data=obj, cls=CapacityRule)

    def get(self, rule_id: str) -> CapacityRule:
        data = self._http.get(f"{_BASE}/{rule_id}")
        obj = data.get("data", data) if isinstance(data, dict) else data
        return to_domain(data=obj, cls=CapacityRule)

    def create(self, entity: CreateCapacityRuleCmd) -> CapacityRule:
        payload = to_payload_create(entity)
        data = self._http.post(_BASE, payload)
        obj = data.get("data", data) if isinstance(data, dict) else data
        return to_domain(data=obj, cls=CapacityRule)

    def update(self, rule_id: str, entity: UpdateCapacityRuleCmd) -> CapacityRule:
        payload = to_payload_update(entity)
        data = self._http.put(f"{_BASE}/{rule_id}", payload)
        obj = data.get("data", data) if isinstance(data, dict) else data
        return to_domain(data=obj, cls=CapacityRule)

    def delete(self, rule_id: str) -> None:
        self._http.delete(f"{_BASE}/{rule_id}")

    def assign_agents(self, rule_id: str, agent_ids: list[int]) -> dict:
        payload = {"agents": agent_ids}
        return self._http.patch(f"{_BASE}/{rule_id}/agents", payload)

    def list_assignees(self) -> Iterable[CapacityRuleAssignee]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/assignees",
            base_url=self._http.base_url,
            items_key="assignees",
        ):
            yield to_domain(data=obj, cls=CapacityRuleAssignee)

    def list_rule_assignees(self, rule_id: str) -> Iterable[CapacityRuleAssignee]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/{rule_id}/assignees",
            base_url=self._http.base_url,
            items_key="assignees",
        ):
            yield to_domain(data=obj, cls=CapacityRuleAssignee)
