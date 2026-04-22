import itertools

import pytest

from libzapi import Ticketing


def _first_ticket_id(ticketing: Ticketing) -> int:
    for ticket in itertools.islice(ticketing.tickets.list(), 50):
        return ticket.id
    pytest.skip("No tickets available for comment tests.")


def test_list_for_ticket(ticketing: Ticketing):
    ticket_id = _first_ticket_id(ticketing)
    comments = list(
        itertools.islice(ticketing.ticket_comments.list_for_ticket(ticket_id), 10)
    )
    assert isinstance(comments, list)
    for comment in comments:
        assert comment.id > 0
        assert comment.type == "Comment" or comment.type == "VoiceComment"


def test_list_for_ticket_with_sort_desc(ticketing: Ticketing):
    ticket_id = _first_ticket_id(ticketing)
    comments = list(
        itertools.islice(
            ticketing.ticket_comments.list_for_ticket(
                ticket_id, sort_order="desc"
            ),
            5,
        )
    )
    assert isinstance(comments, list)


def test_count_for_ticket(ticketing: Ticketing):
    ticket_id = _first_ticket_id(ticketing)
    count = ticketing.ticket_comments.count(ticket_id)
    assert isinstance(count, int)
    assert count >= 0
