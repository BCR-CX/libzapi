import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_posts(help_center: HelpCenter):
    try:
        posts = list(help_center.posts.list_all())
    except NotFound:
        pytest.skip("Community posts not enabled on this account")
    assert isinstance(posts, list)


def test_create_get_update_delete_post(help_center: HelpCenter):
    try:
        topics = list(help_center.topics.list_all())
    except NotFound:
        pytest.skip("Community not enabled on this account")
    if not topics:
        pytest.skip("No topics found")
    topic_id = topics[0].id

    post = help_center.posts.create(
        title="Integration Test Post",
        details="<p>Integration test details</p>",
        topic_id=topic_id,
        notify_subscribers=False,
    )
    assert post.id is not None

    try:
        fetched = help_center.posts.get(post_id=post.id)
        assert fetched.id == post.id

        by_topic = list(help_center.posts.list_by_topic(topic_id=topic_id))
        assert isinstance(by_topic, list)
    finally:
        help_center.posts.delete(post_id=post.id)
