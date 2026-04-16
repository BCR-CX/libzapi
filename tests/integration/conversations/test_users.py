import uuid

from libzapi import Conversations


def test_create_get_delete_user(conversations: Conversations):
    ext_id = f"sdk-test-{uuid.uuid4().hex[:8]}"
    user = conversations.users.create(external_id=ext_id)
    assert user.id is not None
    try:
        fetched = conversations.users.get(user.id)
        assert fetched.id == user.id
    finally:
        conversations.users.delete(user.id)
