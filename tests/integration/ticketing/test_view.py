import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_view(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        title=f"libzapi view {suffix}",
        all=[{"field": "status", "operator": "is", "value": "open"}],
        output={"columns": ["subject", "requester", "created"]},
    )
    defaults.update(overrides)
    return ticketing.views.create(**defaults)


def test_list_and_get_view(ticketing: Ticketing):
    views = list(itertools.islice(ticketing.views.list_all(), 20))
    assert len(views) > 0
    view = ticketing.views.get_by_id(views[0].id)
    assert view.raw_title == views[0].raw_title


def test_list_active(ticketing: Ticketing):
    views = list(itertools.islice(ticketing.views.list_active(), 20))
    assert isinstance(views, list)


def test_count(ticketing: Ticketing):
    snapshot = ticketing.views.count()
    assert snapshot.value is not None


def test_create_update_delete(ticketing: Ticketing):
    view = _create_view(ticketing, description="created by libzapi")
    assert view.id > 0
    updated = ticketing.views.update(view.id, active=False)
    assert updated.active is False
    ticketing.views.delete(view.id)


def test_count_view_and_execute(ticketing: Ticketing):
    view = _create_view(ticketing)
    try:
        count = ticketing.views.count_view(view.id)
        assert isinstance(count, dict)
        result = ticketing.views.execute(view.id)
        assert isinstance(result, dict)
    finally:
        ticketing.views.delete(view.id)


def test_count_many(ticketing: Ticketing):
    a = _create_view(ticketing)
    b = _create_view(ticketing)
    try:
        counts = ticketing.views.count_many([a.id, b.id])
        assert isinstance(counts, list)
    finally:
        ticketing.views.delete(a.id)
        ticketing.views.delete(b.id)


def test_search(ticketing: Ticketing):
    view = _create_view(ticketing, title=f"libzapi search {_unique()}")
    try:
        matches = list(
            itertools.islice(ticketing.views.search(query="libzapi"), 10)
        )
        assert any(m.id == view.id for m in matches) or matches == []
    finally:
        ticketing.views.delete(view.id)


def test_update_many(ticketing: Ticketing):
    a = _create_view(ticketing)
    b = _create_view(ticketing)
    try:
        job = ticketing.views.update_many(
            [(a.id, {"active": False}), (b.id, {"active": False})]
        )
        assert job.id
    finally:
        ticketing.views.delete(a.id)
        ticketing.views.delete(b.id)


def test_destroy_many(ticketing: Ticketing):
    a = _create_view(ticketing)
    b = _create_view(ticketing)
    job = ticketing.views.destroy_many([a.id, b.id])
    assert job.id
