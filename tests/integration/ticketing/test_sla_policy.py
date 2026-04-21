import itertools
import uuid

from libzapi import Ticketing


_METRICS = [
    {
        "priority": "low",
        "metric": "first_reply_time",
        "target": 480,
        "business_hours": False,
    }
]


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_policy(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        title=f"libzapi sla {suffix}",
        filter={
            "all": [{"field": "type", "operator": "is", "value": "incident"}],
            "any": [],
        },
        policy_metrics=list(_METRICS),
    )
    defaults.update(overrides)
    return ticketing.sla_policies.create(**defaults)


def test_list_and_get_sla_policy(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.sla_policies.list(), 20))
    assert len(items) > 0
    item = ticketing.sla_policies.get(items[0].id)
    assert item.title == items[0].title


def test_list_definitions(ticketing: Ticketing):
    defs = ticketing.sla_policies.list_definitions()
    assert isinstance(defs, dict)


def test_create_update_delete(ticketing: Ticketing):
    policy = _create_policy(ticketing, description="created by libzapi")
    assert policy.id > 0
    updated = ticketing.sla_policies.update(
        policy.id, description="updated by libzapi"
    )
    assert updated.description == "updated by libzapi"
    ticketing.sla_policies.delete(policy.id)


def test_reorder(ticketing: Ticketing):
    a = _create_policy(ticketing)
    b = _create_policy(ticketing)
    try:
        reordered = ticketing.sla_policies.reorder([b.id, a.id])
        assert isinstance(reordered, list)
    finally:
        ticketing.sla_policies.delete(a.id)
        ticketing.sla_policies.delete(b.id)
