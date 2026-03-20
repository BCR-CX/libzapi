from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class CapacityRuleAssignee:
    agent_id: int
    capacity_rule_id: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("capacity_rule_assignee", str(self.agent_id))
