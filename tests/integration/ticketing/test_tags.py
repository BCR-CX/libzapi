import itertools
import uuid

import pytest

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _first_ticket_id(ticketing: Ticketing) -> int:
    for ticket in itertools.islice(ticketing.tickets.list(), 50):
        return ticket.id
    pytest.skip("No tickets available to tag.")


def test_list_account_tags(ticketing: Ticketing):
    tags = list(itertools.islice(ticketing.tags.list_account(), 20))
    assert isinstance(tags, list)
    for tag in tags:
        assert "name" in tag


def test_list_for_ticket(ticketing: Ticketing):
    ticket_id = _first_ticket_id(ticketing)
    tags = ticketing.tags.list_for("ticket", ticket_id)
    assert isinstance(tags, list)
    for tag in tags:
        assert isinstance(tag, str)


def test_add_set_remove_lifecycle_ticket(ticketing: Ticketing):
    ticket_id = _first_ticket_id(ticketing)
    marker = f"libzapi_{_unique()}"
    try:
        added = ticketing.tags.add("ticket", ticket_id, [marker])
        assert marker in added

        replaced = ticketing.tags.set("ticket", ticket_id, [marker, f"{marker}_b"])
        assert marker in replaced
        assert f"{marker}_b" in replaced

        removed = ticketing.tags.remove(
            "ticket", ticket_id, [marker, f"{marker}_b"]
        )
        assert isinstance(removed, list)
        assert marker not in removed
        assert f"{marker}_b" not in removed
    finally:
        ticketing.tags.remove("ticket", ticket_id, [marker, f"{marker}_b"])


def test_invalid_resource_raises(ticketing: Ticketing):
    with pytest.raises(ValueError):
        ticketing.tags.list_for("group", 1)
