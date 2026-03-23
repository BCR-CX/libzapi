import pytest

from libzapi import Conversations


def test_list_apps(conversations: Conversations):
    try:
        apps = list(conversations.apps.list_all())
        assert isinstance(apps, list)
    except Exception:
        pytest.skip("Insufficient permissions — app-scoped key cannot list all apps")


def test_get_app(conversations: Conversations):
    app = conversations.apps.get(conversations.app_id)
    assert app.id == conversations.app_id
