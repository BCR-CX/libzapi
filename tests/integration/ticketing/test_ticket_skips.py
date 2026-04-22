import itertools

from libzapi import Ticketing


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.ticket_skips.list_all(), 20))
    assert isinstance(items, list)


def test_list_by_user_returns_iterable(ticketing: Ticketing):
    skips = list(itertools.islice(ticketing.ticket_skips.list_all(), 1))
    if not skips:
        import pytest

        pytest.skip("No ticket skips on this tenant.")
    user_id = skips[0].user_id
    items = list(
        itertools.islice(ticketing.ticket_skips.list_by_user(user_id), 20)
    )
    assert isinstance(items, list)


def test_list_by_ticket_returns_iterable(ticketing: Ticketing):
    skips = list(itertools.islice(ticketing.ticket_skips.list_all(), 1))
    if not skips:
        import pytest

        pytest.skip("No ticket skips on this tenant.")
    ticket_id = skips[0].ticket_id
    items = list(
        itertools.islice(ticketing.ticket_skips.list_by_ticket(ticket_id), 20)
    )
    assert isinstance(items, list)
