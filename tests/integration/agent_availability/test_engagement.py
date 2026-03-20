import pytest

from libzapi import AgentAvailability


def test_list_engagements(agent_availability: AgentAvailability):
    engagements = list(agent_availability.engagements.list_all(page_size=10))
    if not engagements:
        pytest.skip("No engagements found in the live API")
    engagement = agent_availability.engagements.get(engagements[0].engagement_id)
    assert engagement.engagement_id == engagements[0].engagement_id
