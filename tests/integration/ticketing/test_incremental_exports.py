import itertools

from libzapi import Ticketing

_EPOCH = 0


def test_tickets(ticketing: Ticketing):
    items = list(
        itertools.islice(ticketing.incremental_exports.tickets(start_time=_EPOCH), 10)
    )
    assert isinstance(items, list)


def test_tickets_cursor(ticketing: Ticketing):
    items = list(
        itertools.islice(
            ticketing.incremental_exports.tickets_cursor(start_time=_EPOCH), 10
        )
    )
    assert isinstance(items, list)


def test_ticket_events(ticketing: Ticketing):
    items = list(
        itertools.islice(
            ticketing.incremental_exports.ticket_events(start_time=_EPOCH), 10
        )
    )
    assert isinstance(items, list)


def test_users(ticketing: Ticketing):
    items = list(
        itertools.islice(ticketing.incremental_exports.users(start_time=_EPOCH), 10)
    )
    assert isinstance(items, list)


def test_organizations(ticketing: Ticketing):
    items = list(
        itertools.islice(
            ticketing.incremental_exports.organizations(start_time=_EPOCH), 10
        )
    )
    assert isinstance(items, list)


def test_sample(ticketing: Ticketing):
    payload = ticketing.incremental_exports.sample(
        resource="tickets", start_time=_EPOCH
    )
    assert isinstance(payload, dict)
    assert "tickets" in payload or "count" in payload
