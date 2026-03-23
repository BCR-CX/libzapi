import uuid

from libzapi import Conversations


def test_list_devices(conversations: Conversations):
    ext_id = f"sdk-test-{uuid.uuid4().hex[:8]}"
    user = conversations.users.create(external_id=ext_id)
    try:
        devices = list(conversations.devices.list_all(user.id))
        assert isinstance(devices, list)
    finally:
        conversations.users.delete(user.id)
