import pytest

from libzapi import HelpCenter


def test_list_article_attachments(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found in the live API")
    attachments = list(help_center.articles_attachments.list_inline(articles[0].id))
    assert isinstance(attachments, list)
