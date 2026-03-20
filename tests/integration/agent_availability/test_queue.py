import pytest

from libzapi import AgentAvailability


def test_list_and_get_queue(agent_availability: AgentAvailability):
    queues = list(agent_availability.queues.list_all())
    if not queues:
        pytest.skip("No queues found in the live API")
    queue = agent_availability.queues.get(queues[0].id)
    assert queue.id == queues[0].id


def test_list_definitions(agent_availability: AgentAvailability):
    definitions = agent_availability.queues.list_definitions()
    assert definitions is not None
