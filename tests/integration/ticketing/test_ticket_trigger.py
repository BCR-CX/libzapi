import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _first_category_id(ticketing: Ticketing) -> str | None:
    cats = list(
        itertools.islice(ticketing.ticket_trigger_categories.list(), 1)
    )
    return str(cats[0].id) if cats else None


def _create_trigger(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        title=f"libzapi trigger {suffix}",
        actions=[{"field": "status", "value": "open"}],
        conditions={
            "all": [{"field": "update_type", "operator": "is", "value": "Create"}],
            "any": [],
        },
    )
    cat = _first_category_id(ticketing)
    if cat is not None:
        defaults["category_id"] = cat
    defaults.update(overrides)
    return ticketing.ticket_triggers.create(**defaults)


def test_list_and_get_ticket_triggers(ticketing: Ticketing):
    triggers = list(itertools.islice(ticketing.ticket_triggers.list(), 20))
    assert len(triggers) > 0
    trigger = ticketing.ticket_triggers.get(triggers[0].id)
    assert trigger.title == triggers[0].title


def test_list_active(ticketing: Ticketing):
    triggers = list(
        itertools.islice(ticketing.ticket_triggers.list_active(), 20)
    )
    assert isinstance(triggers, list)


def test_list_definitions(ticketing: Ticketing):
    defs = ticketing.ticket_triggers.list_definitions()
    assert isinstance(defs, dict)


def test_create_update_delete(ticketing: Ticketing):
    trigger = _create_trigger(ticketing, description="created by libzapi")
    assert trigger.id > 0
    updated = ticketing.ticket_triggers.update(
        trigger.id, description="updated by libzapi", active=False
    )
    assert updated.description == "updated by libzapi"
    assert updated.active is False
    ticketing.ticket_triggers.delete(trigger.id)


def test_search(ticketing: Ticketing):
    trigger = _create_trigger(
        ticketing, title=f"libzapi search {_unique()}"
    )
    try:
        matches = list(
            itertools.islice(
                ticketing.ticket_triggers.search(query="libzapi"), 10
            )
        )
        assert any(m.id == trigger.id for m in matches) or matches == []
    finally:
        ticketing.ticket_triggers.delete(trigger.id)


def test_update_many(ticketing: Ticketing):
    a = _create_trigger(ticketing)
    b = _create_trigger(ticketing)
    try:
        job = ticketing.ticket_triggers.update_many(
            [(a.id, {"active": False}), (b.id, {"active": False})]
        )
        assert job.id
    finally:
        ticketing.ticket_triggers.delete(a.id)
        ticketing.ticket_triggers.delete(b.id)


def test_destroy_many(ticketing: Ticketing):
    a = _create_trigger(ticketing)
    b = _create_trigger(ticketing)
    job = ticketing.ticket_triggers.destroy_many([a.id, b.id])
    assert job.id
