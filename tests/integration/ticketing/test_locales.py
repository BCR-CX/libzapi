import itertools

from libzapi import Ticketing


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.locales.list_all(), 20))
    assert isinstance(items, list)


def test_list_public(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.locales.list_public(), 20))
    assert isinstance(items, list)


def test_get_current(ticketing: Ticketing):
    locale = ticketing.locales.get_current()
    assert locale.id is not None
    assert locale.locale
