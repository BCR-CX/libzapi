import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def _get_or_create_post(help_center: HelpCenter):
    try:
        posts = list(help_center.posts.list_all())
    except NotFound:
        pytest.skip("Community not enabled on this account")
    if posts:
        return posts[0], False
    try:
        topics = list(help_center.topics.list_all())
    except NotFound:
        pytest.skip("Community not enabled on this account")
    if not topics:
        pytest.skip("No topics found to create a post in")
    post = help_center.posts.create(
        title="Temp Post for Comment Test",
        details="<p>Temp</p>",
        topic_id=topics[0].id,
        notify_subscribers=False,
    )
    return post, True


def test_list_post_comments(help_center: HelpCenter):
    post, created = _get_or_create_post(help_center)
    try:
        comments = list(help_center.post_comments.list_by_post(post.id))
        assert isinstance(comments, list)
    finally:
        if created:
            help_center.posts.delete(post_id=post.id)


def test_create_get_update_delete_post_comment(help_center: HelpCenter):
    post, created = _get_or_create_post(help_center)
    try:
        comment = help_center.post_comments.create(
            post_id=post.id,
            body="Integration test post comment",
            notify_subscribers=False,
        )
        assert comment.id is not None

        try:
            fetched = help_center.post_comments.get(post_id=post.id, comment_id=comment.id)
            assert fetched.id == comment.id

            updated = help_center.post_comments.update(
                post_id=post.id,
                comment_id=comment.id,
                body="Updated integration test comment",
            )
            assert updated.body == "Updated integration test comment"
        finally:
            help_center.post_comments.delete(post_id=post.id, comment_id=comment.id)
    finally:
        if created:
            help_center.posts.delete(post_id=post.id)
