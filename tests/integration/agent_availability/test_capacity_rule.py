import pytest

from libzapi import AgentAvailability


def test_list_and_get_capacity_rule(agent_availability: AgentAvailability):
    rules = list(agent_availability.capacity_rules.list_all())
    if not rules:
        pytest.skip("No capacity rules found in the live API")
    rule = agent_availability.capacity_rules.get(rules[0].id)
    assert rule.id == rules[0].id
