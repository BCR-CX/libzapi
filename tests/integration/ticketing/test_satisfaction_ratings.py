import itertools

from libzapi import Ticketing


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.satisfaction_ratings.list_all(), 50))
    assert isinstance(items, list)


def test_list_received(ticketing: Ticketing):
    items = list(
        itertools.islice(ticketing.satisfaction_ratings.list_received(), 50)
    )
    assert isinstance(items, list)


def test_list_filter_by_score(ticketing: Ticketing):
    items = list(
        itertools.islice(
            ticketing.satisfaction_ratings.list_all(score="received"), 50
        )
    )
    assert isinstance(items, list)


def test_list_reasons(ticketing: Ticketing):
    reasons = list(itertools.islice(ticketing.satisfaction_ratings.list_reasons(), 50))
    assert isinstance(reasons, list)
    for reason in reasons:
        assert reason.id > 0
        assert reason.value is not None


def test_get_first_rating(ticketing: Ticketing):
    first = next(iter(ticketing.satisfaction_ratings.list_all()), None)
    if first is None:
        return
    fetched = ticketing.satisfaction_ratings.get_by_id(first.id)
    assert fetched.id == first.id


def test_get_first_reason(ticketing: Ticketing):
    first = next(iter(ticketing.satisfaction_ratings.list_reasons()), None)
    if first is None:
        return
    fetched = ticketing.satisfaction_ratings.get_reason(first.id)
    assert fetched.id == first.id
