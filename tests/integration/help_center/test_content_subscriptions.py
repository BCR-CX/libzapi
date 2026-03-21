import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound, UnprocessableEntity


def test_list_article_subscriptions(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    try:
        subs = list(help_center.content_subscriptions.list("articles", articles[0].id))
    except NotFound:
        pytest.skip("Content subscriptions not available for this article")
    assert isinstance(subs, list)


def test_create_get_delete_article_subscription(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")

    try:
        sub = help_center.content_subscriptions.create("articles", articles[0].id, locale="en-us")
    except (NotFound, UnprocessableEntity):
        pytest.skip("Content subscriptions not available or already subscribed")

    assert sub.id is not None

    try:
        fetched = help_center.content_subscriptions.get("articles", articles[0].id, sub.id)
        assert fetched.id == sub.id
    finally:
        help_center.content_subscriptions.delete("articles", articles[0].id, sub.id)
