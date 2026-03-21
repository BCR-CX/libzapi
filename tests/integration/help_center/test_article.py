import time

import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_articles(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    assert len(articles) > 0, "Expected at least one article from the live API"


def test_list_articles_by_locale(help_center: HelpCenter):
    articles = list(help_center.articles.list_all_by_locale("en-us"))
    assert isinstance(articles, list)


def test_list_articles_by_category(help_center: HelpCenter):
    categories = list(help_center.categories.list_all())
    if not categories:
        pytest.skip("No categories found")
    articles = list(help_center.articles.list_by_category(categories[0].id))
    assert isinstance(articles, list)


def test_list_articles_by_section(help_center: HelpCenter):
    sections = list(help_center.sections.list_all())
    if not sections:
        pytest.skip("No sections found")
    articles = list(help_center.articles.list_by_section(sections[0].id))
    assert isinstance(articles, list)


def test_list_incremental_articles(help_center: HelpCenter):
    one_year_ago = int(time.time()) - 365 * 24 * 60 * 60
    try:
        articles = list(help_center.articles.list_incremental(start_time=one_year_ago))
    except NotFound:
        pytest.skip("Incremental articles endpoint not available")
    assert isinstance(articles, list)


def test_create_get_delete_article(help_center: HelpCenter):
    sections = list(help_center.sections.list_all())
    if not sections:
        pytest.skip("No sections found to create article in")
    section_id = sections[0].id

    pgs = list(help_center.permission_groups.list_all())
    if not pgs:
        pytest.skip("No permission groups found")
    segments = list(help_center.user_segments.list_all())

    article = help_center.articles.create(
        section_id=section_id,
        title="Integration Test Article",
        body="<p>Test body</p>",
        locale="en-us",
        permission_group_id=pgs[0].id,
        user_segment_id=segments[0].id if segments else None,
    )
    assert article.id is not None

    try:
        fetched = help_center.articles.get(article_id=article.id)
        assert fetched.id == article.id
        assert fetched.title == "Integration Test Article"

        user_articles = list(help_center.articles.list_by_user(article.author_id))
        assert isinstance(user_articles, list)
    finally:
        help_center.articles.delete(article_id=article.id)
