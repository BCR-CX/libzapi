import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_topics(help_center: HelpCenter):
    try:
        topics = list(help_center.topics.list_all())
    except NotFound:
        pytest.skip("Community topics not enabled on this account")
    assert isinstance(topics, list)


def test_create_get_update_delete_topic(help_center: HelpCenter):
    try:
        topic = help_center.topics.create(
            name="Integration Test Topic",
            description="Created by integration tests",
        )
    except NotFound:
        pytest.skip("Community topics not enabled on this account")
    assert topic.id is not None

    try:
        fetched = help_center.topics.get(topic_id=topic.id)
        assert fetched.id == topic.id

        updated = help_center.topics.update(topic_id=topic.id, name="Updated Integration Test Topic")
        assert updated.name == "Updated Integration Test Topic"
    finally:
        help_center.topics.delete(topic_id=topic.id)
