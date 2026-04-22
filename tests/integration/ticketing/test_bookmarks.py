import itertools

from libzapi import Ticketing


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.bookmarks.list_all(), 20))
    assert isinstance(items, list)
