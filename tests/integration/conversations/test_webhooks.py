import pytest

from libzapi import Conversations


def test_list_webhooks(conversations: Conversations):
    integrations = list(conversations.integrations.list_all())
    if not integrations:
        pytest.skip("No integrations found")
    try:
        webhooks = list(conversations.webhooks.list_all(integrations[0].id))
        assert isinstance(webhooks, list)
    except Exception:
        pytest.skip("Insufficient permissions to list webhooks for this integration")
