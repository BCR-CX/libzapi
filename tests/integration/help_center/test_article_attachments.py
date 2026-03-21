import pytest

from libzapi import HelpCenter


def _get_first_article(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found in the live API")
    return articles[0]


def test_list_article_attachments_all(help_center: HelpCenter):
    article = _get_first_article(help_center)
    attachments = list(help_center.articles_attachments.list_all(article.id))
    assert isinstance(attachments, list)


def test_list_article_attachments_inline(help_center: HelpCenter):
    article = _get_first_article(help_center)
    attachments = list(help_center.articles_attachments.list_inline(article.id))
    assert isinstance(attachments, list)


def test_list_article_attachments_block(help_center: HelpCenter):
    article = _get_first_article(help_center)
    attachments = list(help_center.articles_attachments.list_block(article.id))
    assert isinstance(attachments, list)


def test_create_get_delete_article_attachment(help_center: HelpCenter):
    article = _get_first_article(help_center)
    attachment = help_center.articles_attachments.create(
        article_id=article.id,
        file=("test_integration.txt", b"integration test content", "text/plain"),
    )
    assert attachment.id is not None

    try:
        fetched = help_center.articles_attachments.get(article_attachment_id=attachment.id)
        assert fetched.id == attachment.id
    finally:
        help_center.articles_attachments.delete(article_attachment_id=attachment.id)
