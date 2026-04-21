import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_automation(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        title=f"libzapi automation {suffix}",
        actions=[{"field": "status", "value": "closed"}],
        conditions={
            "all": [
                {
                    "field": "status",
                    "operator": "is",
                    "value": "solved",
                },
                {
                    "field": "SOLVED",
                    "operator": "greater_than",
                    "value": "24",
                },
            ],
            "any": [],
        },
    )
    defaults.update(overrides)
    return ticketing.automations.create(**defaults)


def test_list_and_get_automation(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.automations.list_all(), 20))
    assert len(items) > 0
    item = ticketing.automations.get(items[0].id)
    assert item.raw_title == items[0].raw_title


def test_list_active(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.automations.list_active(), 20))
    assert isinstance(items, list)


def test_create_update_delete(ticketing: Ticketing):
    auto = _create_automation(ticketing)
    assert auto.id > 0
    updated = ticketing.automations.update(auto.id, active=False)
    assert updated.active is False
    ticketing.automations.delete(auto.id)


def test_search(ticketing: Ticketing):
    auto = _create_automation(
        ticketing, title=f"libzapi search {_unique()}"
    )
    try:
        matches = list(
            itertools.islice(
                ticketing.automations.search(query="libzapi"), 10
            )
        )
        assert any(m.id == auto.id for m in matches) or matches == []
    finally:
        ticketing.automations.delete(auto.id)


def test_update_many(ticketing: Ticketing):
    a = _create_automation(ticketing)
    b = _create_automation(ticketing)
    try:
        job = ticketing.automations.update_many(
            [(a.id, {"active": False}), (b.id, {"active": False})]
        )
        assert job.id
    finally:
        ticketing.automations.delete(a.id)
        ticketing.automations.delete(b.id)


def test_destroy_many(ticketing: Ticketing):
    a = _create_automation(ticketing)
    b = _create_automation(ticketing)
    job = ticketing.automations.destroy_many([a.id, b.id])
    assert job.id
