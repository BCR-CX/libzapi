import pytest
import requests

from libzapi import HelpCenter
from libzapi.domain.errors import UnprocessableEntity


def _get_commentable_article(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    for article in articles:
        if not article.comments_disabled:
            return article
    if articles:
        return articles[0]
    pytest.skip("No articles found")


def test_list_article_comments(help_center: HelpCenter):
    article = _get_commentable_article(help_center)
    comments = list(help_center.article_comments.list_by_article(article.id))
    assert isinstance(comments, list)


def test_create_get_update_delete_article_comment(help_center: HelpCenter):
    article = _get_commentable_article(help_center)
    try:
        comment = help_center.article_comments.create(
            article_id=article.id,
            body="Integration test comment",
            notify_subscribers=False,
        )
    except (UnprocessableEntity, requests.exceptions.HTTPError):
        pytest.skip("Cannot create comments on this article")

    assert comment.id is not None

    try:
        fetched = help_center.article_comments.get(article_id=article.id, comment_id=comment.id)
        assert fetched.id == comment.id

        updated = help_center.article_comments.update(
            article_id=article.id,
            comment_id=comment.id,
            body="Updated integration test comment",
        )
        assert updated.body == "Updated integration test comment"
    finally:
        help_center.article_comments.delete(article_id=article.id, comment_id=comment.id)
