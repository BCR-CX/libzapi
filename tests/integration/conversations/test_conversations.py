import uuid

from libzapi import Conversations


def test_create_get_list_conversation(conversations: Conversations):
    ext_id = f"sdk-test-{uuid.uuid4().hex[:8]}"
    user = conversations.users.create(external_id=ext_id)
    try:
        conv = conversations.conversations_.create(type="personal", participants=[{"userId": user.id}])
        assert conv.id is not None

        fetched = conversations.conversations_.get(conv.id)
        assert fetched.id == conv.id

        convs = list(conversations.conversations_.list_by_user(user.id))
        assert isinstance(convs, list)
        assert any(c.id == conv.id for c in convs)
    finally:
        # Deleting the user also removes their personal conversations
        conversations.users.delete(user.id)
