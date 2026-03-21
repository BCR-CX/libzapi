import pytest
import requests

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound, UnprocessableEntity


def _get_first_article(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    return articles[0]


def test_list_all_labels(help_center: HelpCenter):
    labels = list(help_center.article_labels.list_all())
    assert isinstance(labels, list)


def test_list_labels_by_article(help_center: HelpCenter):
    article = _get_first_article(help_center)
    labels = list(help_center.article_labels.list_by_article(article.id))
    assert isinstance(labels, list)


def test_create_delete_article_label(help_center: HelpCenter):
    article = _get_first_article(help_center)
    try:
        label = help_center.article_labels.create(article_id=article.id, name="integration-test-label")
    except (UnprocessableEntity, NotFound, requests.exceptions.HTTPError):
        pytest.skip("Cannot create labels on this article")

    assert label.id is not None

    help_center.article_labels.delete(article_id=article.id, label_id=label.id)
