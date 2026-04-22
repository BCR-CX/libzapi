import itertools

from libzapi import Ticketing


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.ticket_activities.list_all(), 20))
    assert isinstance(items, list)


def test_list_with_include(ticketing: Ticketing):
    items = list(
        itertools.islice(
            ticketing.ticket_activities.list_all(include="users"), 20
        )
    )
    assert isinstance(items, list)


def test_get_first_activity(ticketing: Ticketing):
    first = next(iter(ticketing.ticket_activities.list_all()), None)
    if first is None:
        return
    fetched = ticketing.ticket_activities.get_by_id(first.id)
    assert fetched.id == first.id
