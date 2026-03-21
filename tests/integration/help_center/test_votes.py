import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_article_votes(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    try:
        votes = list(help_center.votes.list_article_votes(articles[0].id))
    except NotFound:
        pytest.skip("Votes not available for this article")
    assert isinstance(votes, list)


def test_up_and_down_article(help_center: HelpCenter):
    articles = list(help_center.articles.list_all())
    if not articles:
        pytest.skip("No articles found")
    try:
        vote = help_center.votes.up_article(articles[0].id)
    except NotFound:
        pytest.skip("Voting not available for this article")
    assert vote.id is not None
    assert vote.value == 1

    fetched = help_center.votes.get(vote_id=vote.id)
    assert fetched.id == vote.id

    help_center.votes.delete(vote_id=vote.id)
