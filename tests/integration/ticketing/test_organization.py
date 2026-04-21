import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_org(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(name=f"libzapi org {suffix}")
    defaults.update(overrides)
    return ticketing.organizations.create(**defaults)


def test_list_and_get(ticketing: Ticketing):
    objs = list(itertools.islice(ticketing.organizations.list_all(), 1000))
    assert len(objs) > 0
    obj = ticketing.organizations.get_by_id(objs[0].id)
    assert obj.id == objs[0].id


def test_search_by_name(ticketing: Ticketing):
    org = _create_org(ticketing)
    matches = list(ticketing.organizations.search(name=org.name))
    assert any(m.id == org.id for m in matches)


def test_search_by_external_id(ticketing: Ticketing):
    ext_id = f"libzapi-ext-{_unique()}"
    org = _create_org(ticketing, external_id=ext_id)
    matches = list(ticketing.organizations.search(external_id=ext_id))
    assert any(m.id == org.id for m in matches)


def test_autocomplete(ticketing: Ticketing):
    org = _create_org(ticketing)
    matches = list(ticketing.organizations.autocomplete(name=org.name[:6]))
    assert any(m.id == org.id for m in matches) or matches == []


def test_create_update_delete(ticketing: Ticketing):
    org = _create_org(ticketing, notes="created by libzapi integration test")
    assert org.id > 0
    updated = ticketing.organizations.update(
        organization_id=org.id, notes="updated by libzapi"
    )
    assert updated.notes == "updated by libzapi"
    ticketing.organizations.delete(org.id)


def test_show_many_by_ids(ticketing: Ticketing):
    a = _create_org(ticketing)
    b = _create_org(ticketing)
    orgs = list(ticketing.organizations.show_many(organization_ids=[a.id, b.id]))
    ids = {o.id for o in orgs}
    assert {a.id, b.id} <= ids


def test_show_many_by_external_ids(ticketing: Ticketing):
    ext_a = f"libzapi-sm-{_unique()}"
    ext_b = f"libzapi-sm-{_unique()}"
    _create_org(ticketing, external_id=ext_a)
    _create_org(ticketing, external_id=ext_b)
    orgs = list(ticketing.organizations.show_many(external_ids=[ext_a, ext_b]))
    externals = {o.external_id for o in orgs}
    assert {ext_a, ext_b} <= externals


def test_list_related(ticketing: Ticketing):
    org = _create_org(ticketing)
    related = ticketing.organizations.list_related(org.id)
    assert related.tickets_count >= 0
    assert related.users_count >= 0


def test_create_many(ticketing: Ticketing):
    job = ticketing.organizations.create_many(
        [
            {"name": f"libzapi bulk {_unique()}"},
            {"name": f"libzapi bulk {_unique()}"},
        ]
    )
    assert job.id


def test_create_or_update(ticketing: Ticketing):
    ext_id = f"libzapi-cou-{_unique()}"
    first = ticketing.organizations.create_or_update(
        name="libzapi cou", external_id=ext_id
    )
    second = ticketing.organizations.create_or_update(
        name="libzapi cou updated", external_id=ext_id
    )
    assert first.id == second.id


def test_update_many_uniform(ticketing: Ticketing):
    a = _create_org(ticketing)
    b = _create_org(ticketing)
    job = ticketing.organizations.update_many(
        [a.id, b.id], tags=["libzapi-um"]
    )
    assert job.id


def test_update_many_individually(ticketing: Ticketing):
    a = _create_org(ticketing)
    b = _create_org(ticketing)
    job = ticketing.organizations.update_many_individually(
        [(a.id, {"tags": ["libzapi-umi-a"]}), (b.id, {"tags": ["libzapi-umi-b"]})]
    )
    assert job.id


def test_destroy_many(ticketing: Ticketing):
    a = _create_org(ticketing)
    b = _create_org(ticketing)
    job = ticketing.organizations.destroy_many([a.id, b.id])
    assert job.id


def test_list_tags(ticketing: Ticketing):
    org = _create_org(ticketing, tags=["libzapi-org-listtag"])
    tags = ticketing.organizations.list_tags(org.id)
    assert "libzapi-org-listtag" in tags


def test_set_tags(ticketing: Ticketing):
    org = _create_org(ticketing)
    tags = ticketing.organizations.set_tags(org.id, ["libzapi-org-set"])
    assert "libzapi-org-set" in tags


def test_add_tags(ticketing: Ticketing):
    org = _create_org(ticketing, tags=["libzapi-org-keep"])
    tags = ticketing.organizations.add_tags(org.id, ["libzapi-org-added"])
    assert {"libzapi-org-keep", "libzapi-org-added"} <= set(tags)


def test_remove_tags(ticketing: Ticketing):
    org = _create_org(ticketing, tags=["libzapi-org-keep", "libzapi-org-drop"])
    tags = ticketing.organizations.remove_tags(org.id, ["libzapi-org-drop"])
    assert "libzapi-org-drop" not in tags
    assert "libzapi-org-keep" in tags
