import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.custom_ticket_statuses.list_all(), 100))
    assert isinstance(items, list)


def test_list_with_category_filter(ticketing: Ticketing):
    items = list(
        itertools.islice(
            ticketing.custom_ticket_statuses.list_all(status_categories=["open"]),
            50,
        )
    )
    assert isinstance(items, list)
    for item in items:
        assert item.status_category == "open"


def test_list_with_active_filter(ticketing: Ticketing):
    items = list(
        itertools.islice(
            ticketing.custom_ticket_statuses.list_all(active=True), 50
        )
    )
    assert isinstance(items, list)
    for item in items:
        assert item.active is True


def test_create_update_and_fetch(ticketing: Ticketing):
    label = f"libzapi {_unique()}"
    created = ticketing.custom_ticket_statuses.create(
        status_category="pending",
        agent_label=label,
        end_user_label=label,
        description="created by libzapi integration test",
    )
    try:
        assert created.id > 0
        assert created.agent_label == label
        fetched = ticketing.custom_ticket_statuses.get_by_id(created.id)
        assert fetched.id == created.id
        updated = ticketing.custom_ticket_statuses.update(
            status_id=created.id, agent_label=f"{label} updated"
        )
        assert updated.agent_label.endswith("updated")
    finally:
        ticketing.custom_ticket_statuses.update(status_id=created.id, active=False)
