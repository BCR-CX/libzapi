import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_search_articles(help_center: HelpCenter):
    results = list(help_center.search.search_articles("test"))
    assert isinstance(results, list)


def test_search_posts(help_center: HelpCenter):
    try:
        results = list(help_center.search.search_posts("test"))
    except NotFound:
        pytest.skip("Community search not available")
    assert isinstance(results, list)
