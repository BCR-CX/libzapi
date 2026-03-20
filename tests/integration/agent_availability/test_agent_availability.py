import pytest

from libzapi import AgentAvailability


def test_list_and_get_availability(agent_availability: AgentAvailability):
    agents = list(agent_availability.availabilities.list_all())
    if not agents:
        pytest.skip("No agent availabilities found in the live API")
    agent = agent_availability.availabilities.get(agents[0].agent_id)
    assert agent.agent_id == agents[0].agent_id
