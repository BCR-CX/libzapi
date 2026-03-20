from typing import Iterator

from libzapi.application.commands.agent_availability.capacity_rule_cmds import (
    CreateCapacityRuleCmd,
    UpdateCapacityRuleCmd,
)
from libzapi.domain.models.agent_availability.capacity_rule import CapacityRule
from libzapi.domain.models.agent_availability.capacity_rule_assignee import CapacityRuleAssignee
from libzapi.infrastructure.api_clients.agent_availability import CapacityRuleApiClient


class CapacityRulesService:
    """High-level service using the API client."""

    def __init__(self, client: CapacityRuleApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[CapacityRule]:
        return self._client.list()

    def get(self, rule_id: str) -> CapacityRule:
        return self._client.get(rule_id=rule_id)

    def create(self, entity: CreateCapacityRuleCmd) -> CapacityRule:
        return self._client.create(entity=entity)

    def update(self, rule_id: str, entity: UpdateCapacityRuleCmd) -> CapacityRule:
        return self._client.update(rule_id=rule_id, entity=entity)

    def delete(self, rule_id: str) -> None:
        return self._client.delete(rule_id=rule_id)

    def assign_agents(self, rule_id: str, agent_ids: list[int]) -> dict:
        return self._client.assign_agents(rule_id=rule_id, agent_ids=agent_ids)

    def list_assignees(self) -> Iterator[CapacityRuleAssignee]:
        return self._client.list_assignees()

    def list_rule_assignees(self, rule_id: str) -> Iterator[CapacityRuleAssignee]:
        return self._client.list_rule_assignees(rule_id=rule_id)
