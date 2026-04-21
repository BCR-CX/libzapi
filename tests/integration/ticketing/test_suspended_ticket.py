from libzapi import Ticketing


def test_list_and_get(ticketing: Ticketing):
    collection = list(ticketing.suspended_tickets.list_all())
    assert isinstance(collection, list)
    if collection:
        item = ticketing.suspended_tickets.get_by_id(collection[0].id)
        assert item.id == collection[0].id


def test_list_attachments(ticketing: Ticketing):
    collection = list(ticketing.suspended_tickets.list_all())
    if not collection:
        return
    attachments = ticketing.suspended_tickets.list_attachments(
        collection[0].id
    )
    assert isinstance(attachments, list)
