from libzapi.application.commands.agent_availability.capacity_rule_cmds import (
    CreateCapacityRuleCmd,
    UpdateCapacityRuleCmd,
)
from libzapi.application.commands.agent_availability.queue_cmds import CreateQueueCmd, UpdateQueueCmd
from libzapi.infrastructure.mappers.agent_availability.capacity_rule_mapper import (
    to_payload_create as rule_create,
    to_payload_update as rule_update,
)
from libzapi.infrastructure.mappers.agent_availability.queue_mapper import (
    to_payload_create as queue_create,
    to_payload_update as queue_update,
)


# ── Capacity Rule mapper ───────────────────────────────────────────────


def test_capacity_rule_create_all_fields():
    cmd = CreateCapacityRuleCmd(name="Custom Rule", capacities={"messaging": 5}, description="Test rule")
    result = rule_create(cmd)
    assert result == {"name": "Custom Rule", "capacities": {"messaging": 5}, "description": "Test rule"}


def test_capacity_rule_create_minimal():
    cmd = CreateCapacityRuleCmd(name="Basic", capacities={"support": 3})
    result = rule_create(cmd)
    assert result == {"name": "Basic", "capacities": {"support": 3}}
    assert "description" not in result


def test_capacity_rule_update_only_includes_non_none():
    cmd = UpdateCapacityRuleCmd(name="Renamed")
    result = rule_update(cmd)
    assert result == {"name": "Renamed"}


def test_capacity_rule_update_empty():
    cmd = UpdateCapacityRuleCmd()
    result = rule_update(cmd)
    assert result == {}


# ── Queue mapper ───────────────────────────────────────────────────────


def test_queue_create_all_fields():
    cmd = CreateQueueCmd(
        name="Priority Queue",
        definition={"all": [{"field": "type", "operator": "is", "value": "incident"}]},
        priority=1,
        primary_groups={"group_ids": [1, 2]},
        description="High priority",
        secondary_groups={"group_ids": [3]},
    )
    result = queue_create(cmd)
    assert result == {
        "queue": {
            "name": "Priority Queue",
            "definition": {"all": [{"field": "type", "operator": "is", "value": "incident"}]},
            "priority": 1,
            "primary_groups": {"group_ids": [1, 2]},
            "description": "High priority",
            "secondary_groups": {"group_ids": [3]},
        }
    }


def test_queue_create_minimal():
    cmd = CreateQueueCmd(name="Basic", definition={}, priority=1, primary_groups={"group_ids": [1]})
    result = queue_create(cmd)
    assert result == {"queue": {"name": "Basic", "definition": {}, "priority": 1, "primary_groups": {"group_ids": [1]}}}


def test_queue_update_only_includes_non_none():
    cmd = UpdateQueueCmd(name="Renamed", priority=2)
    result = queue_update(cmd)
    assert result == {"queue": {"name": "Renamed", "priority": 2}}


def test_queue_update_empty():
    cmd = UpdateQueueCmd()
    result = queue_update(cmd)
    assert result == {"queue": {}}
