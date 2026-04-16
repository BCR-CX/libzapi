import pytest

from libzapi import Conversations


def test_list_integrations(conversations: Conversations):
    integrations = list(conversations.integrations.list_all())
    assert isinstance(integrations, list)


def test_list_and_get_integration(conversations: Conversations):
    integrations = list(conversations.integrations.list_all())
    if not integrations:
        pytest.skip("No integrations found")
    integration = conversations.integrations.get(integrations[0].id)
    assert integration.id == integrations[0].id
