from libzapi import AgentAvailability


def test_list_all_statuses(agent_availability: AgentAvailability):
    statuses = agent_availability.unified_agent_statuses.list_all()
    assert len(statuses) > 0, "Expected at least one unified agent status"
