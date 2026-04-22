import itertools

import pytest

from libzapi import Ticketing


def test_list_for_ticket_returns_iterable(ticketing: Ticketing):
    tickets = list(itertools.islice(ticketing.tickets.list(), 1))
    if not tickets:
        pytest.skip("No tickets on this tenant.")
    items = list(
        itertools.islice(
            ticketing.side_conversations.list_for_ticket(tickets[0].id), 20
        )
    )
    assert isinstance(items, list)
