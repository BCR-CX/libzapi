from libzapi import Conversations


def test_list_switchboards(conversations: Conversations):
    switchboards = list(conversations.switchboards.list_all())
    assert isinstance(switchboards, list)
