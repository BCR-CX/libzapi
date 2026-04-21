import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


_COND = {"all": [{"field": "status", "operator": "is", "value": "new"}]}


def _create_workspace(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        title=f"libzapi workspace {suffix}",
        conditions=_COND,
    )
    defaults.update(overrides)
    return ticketing.workspaces.create(**defaults)


def test_list_and_get_workspace(ticketing: Ticketing):
    workspaces = list(itertools.islice(ticketing.workspaces.list(), 10))
    if not workspaces:
        return
    ws = ticketing.workspaces.get(workspaces[0].id)
    assert ws.title == workspaces[0].title


def test_create_update_delete_workspace(ticketing: Ticketing):
    ws = _create_workspace(ticketing, description="created by libzapi")
    assert ws.id > 0
    try:
        updated = ticketing.workspaces.update(
            ws.id, description="updated by libzapi", activated=False
        )
        assert updated.description == "updated by libzapi"
    finally:
        ticketing.workspaces.delete(ws.id)


def test_reorder_does_not_raise(ticketing: Ticketing):
    workspaces = list(itertools.islice(ticketing.workspaces.list(), 5))
    ids = [w.id for w in workspaces]
    if ids:
        ticketing.workspaces.reorder(ids)
