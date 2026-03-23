import uuid

from libzapi import Conversations


def test_list_clients(conversations: Conversations):
    ext_id = f"sdk-test-{uuid.uuid4().hex[:8]}"
    user = conversations.users.create(external_id=ext_id)
    try:
        clients = list(conversations.clients.list_all(user.id))
        assert isinstance(clients, list)
    finally:
        conversations.users.delete(user.id)
