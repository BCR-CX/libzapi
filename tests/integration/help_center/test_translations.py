import pytest

from libzapi import HelpCenter


def test_list_article_translations(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    translations = list(help_center.translations.list("articles", articles[0].id))
    assert isinstance(translations, list)


def test_get_article_translation(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    translation = help_center.translations.get("articles", articles[0].id, articles[0].locale)
    assert translation.locale == articles[0].locale


def test_list_missing_translations(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    missing = help_center.translations.list_missing("articles", articles[0].id)
    assert isinstance(missing, list)


def test_list_category_translations(help_center: HelpCenter):
    categories = list(help_center.categories.list_all())
    if not categories:
        pytest.skip("No categories found")
    translations = list(help_center.translations.list("categories", categories[0].id))
    assert isinstance(translations, list)


def test_list_section_translations(help_center: HelpCenter):
    sections = list(help_center.sections.list_all())
    if not sections:
        pytest.skip("No sections found")
    translations = list(help_center.translations.list("sections", sections[0].id))
    assert isinstance(translations, list)
