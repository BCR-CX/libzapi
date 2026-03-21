import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_user_subscriptions(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    try:
        subs = list(help_center.user_subscriptions.list_by_user(articles[0].author_id))
    except NotFound:
        pytest.skip("User subscriptions not available")
    assert isinstance(subs, list)
