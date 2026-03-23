import uuid

from libzapi import Conversations


def test_list_participants(conversations: Conversations):
    ext_id = f"sdk-test-{uuid.uuid4().hex[:8]}"
    user = conversations.users.create(external_id=ext_id)
    try:
        conv = conversations.conversations_.create(type="personal", participants=[{"userId": user.id}])
        participants = list(conversations.participants.list_all(conv.id))
        assert isinstance(participants, list)
        assert len(participants) >= 1
    finally:
        conversations.users.delete(user.id)
