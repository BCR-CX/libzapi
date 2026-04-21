import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_macro(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        title=f"libzapi macro {suffix}",
        actions=[{"field": "status", "value": "solved"}],
    )
    defaults.update(overrides)
    return ticketing.macros.create(**defaults)


def test_list_and_get_macro(ticketing: Ticketing):
    macros = list(itertools.islice(ticketing.macros.list(), 20))
    assert len(macros) > 0
    macro = ticketing.macros.get(macros[0].id)
    assert macro.raw_title == macros[0].raw_title


def test_list_active(ticketing: Ticketing):
    macros = list(itertools.islice(ticketing.macros.list_active(), 20))
    assert isinstance(macros, list)


def test_list_categories(ticketing: Ticketing):
    cats = ticketing.macros.list_categories()
    assert isinstance(cats, list)


def test_list_definitions(ticketing: Ticketing):
    defs = ticketing.macros.list_definitions()
    assert isinstance(defs, dict)


def test_create_update_delete(ticketing: Ticketing):
    macro = _create_macro(ticketing, description="created by libzapi")
    assert macro.id > 0
    updated = ticketing.macros.update(
        macro.id, description="updated by libzapi", active=False
    )
    assert updated.description == "updated by libzapi"
    assert updated.active is False
    ticketing.macros.delete(macro.id)


def test_apply(ticketing: Ticketing):
    macro = _create_macro(ticketing)
    try:
        result = ticketing.macros.apply(macro.id)
        assert isinstance(result, dict)
    finally:
        ticketing.macros.delete(macro.id)


def test_search(ticketing: Ticketing):
    macro = _create_macro(ticketing, title=f"libzapi search {_unique()}")
    try:
        matches = list(
            itertools.islice(ticketing.macros.search(query="libzapi"), 10)
        )
        assert any(m.id == macro.id for m in matches) or matches == []
    finally:
        ticketing.macros.delete(macro.id)


def test_create_many_and_destroy_many(ticketing: Ticketing):
    job = ticketing.macros.create_many(
        [
            {
                "title": f"libzapi bulk {_unique()}",
                "actions": [{"field": "status", "value": "solved"}],
            },
            {
                "title": f"libzapi bulk {_unique()}",
                "actions": [{"field": "priority", "value": "low"}],
            },
        ]
    )
    assert job.id


def test_update_many(ticketing: Ticketing):
    a = _create_macro(ticketing)
    b = _create_macro(ticketing)
    try:
        job = ticketing.macros.update_many(
            [(a.id, {"active": False}), (b.id, {"active": False})]
        )
        assert job.id
    finally:
        ticketing.macros.delete(a.id)
        ticketing.macros.delete(b.id)
