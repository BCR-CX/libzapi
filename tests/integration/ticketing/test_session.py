import itertools

from libzapi import Ticketing


def test_list_sessions(ticketing: Ticketing):
    sessions = list(itertools.islice(ticketing.sessions.list(), 5))
    assert isinstance(sessions, list)


def test_get_current_session(ticketing: Ticketing):
    session = ticketing.sessions.get_current()
    assert session.id > 0


def test_list_by_user(ticketing: Ticketing):
    current = ticketing.sessions.get_current()
    sessions = list(
        itertools.islice(
            ticketing.sessions.list_user(current.user_id), 5
        )
    )
    assert isinstance(sessions, list)
