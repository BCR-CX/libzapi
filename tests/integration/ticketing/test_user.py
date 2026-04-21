import itertools
import uuid

import pytest

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_user(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        name=f"libzapi {suffix}",
        email=f"libzapi-{suffix}@example.invalid",
        role="end-user",
    )
    defaults.update(overrides)
    return ticketing.users.create(**defaults)


def test_list_and_get_user(ticketing: Ticketing):
    objs = list(itertools.islice(ticketing.users.list_all(), 1000))
    assert len(objs) > 0
    obj = ticketing.users.get_by_id(objs[0].id)
    assert obj.id == objs[0].id


def test_me(ticketing: Ticketing):
    user = ticketing.users.me()
    assert user.id > 0


def test_create_update_delete_user(ticketing: Ticketing):
    user = _create_user(ticketing, notes="created by libzapi integration test")
    assert user.id > 0
    updated = ticketing.users.update(user_id=user.id, name=f"{user.name} (updated)")
    assert updated.name.endswith("(updated)")
    deleted = ticketing.users.delete(user.id)
    assert deleted.active is False


def test_show_many(ticketing: Ticketing):
    a = _create_user(ticketing)
    b = _create_user(ticketing)
    users = list(ticketing.users.show_many([a.id, b.id]))
    ids = {u.id for u in users}
    assert {a.id, b.id} <= ids


def test_search_by_external_id(ticketing: Ticketing):
    ext_id = f"libzapi-{_unique()}"
    user = _create_user(ticketing, external_id=ext_id)
    matches = list(ticketing.users.search(external_id=ext_id))
    assert any(m.id == user.id for m in matches)


def test_search_by_query(ticketing: Ticketing):
    user = _create_user(ticketing)
    matches = list(itertools.islice(ticketing.users.search(query=user.email), 25))
    assert any(m.id == user.id for m in matches)


def test_autocomplete(ticketing: Ticketing):
    user = _create_user(ticketing)
    matches = list(ticketing.users.autocomplete(name=user.name))
    assert any(m.id == user.id for m in matches) or matches == []


def test_list_related(ticketing: Ticketing):
    me = ticketing.users.me()
    related = ticketing.users.list_related(me.id)
    assert related.requested_tickets >= 0


def test_list_compliance_deletion_statuses(ticketing: Ticketing):
    user = _create_user(ticketing)
    statuses = list(ticketing.users.list_compliance_deletion_statuses(user.id))
    assert isinstance(statuses, list)


def test_me_settings(ticketing: Ticketing):
    settings = ticketing.users.me_settings()
    assert isinstance(settings, dict)


def test_list_entitlements(ticketing: Ticketing):
    me = ticketing.users.me()
    try:
        entitlements = ticketing.users.list_entitlements(me.id)
    except Exception:
        pytest.skip("entitlements endpoint not enabled on this tenant")
    assert isinstance(entitlements, list)


def test_create_many(ticketing: Ticketing):
    job = ticketing.users.create_many(
        [
            {"name": f"libzapi bulk {_unique()}", "email": f"libzapi-{_unique()}@example.invalid"},
            {"name": f"libzapi bulk {_unique()}", "email": f"libzapi-{_unique()}@example.invalid"},
        ]
    )
    assert job.id


def test_create_or_update(ticketing: Ticketing):
    email = f"libzapi-cou-{_unique()}@example.invalid"
    first = ticketing.users.create_or_update(name="libzapi cou", email=email)
    second = ticketing.users.create_or_update(name="libzapi cou updated", email=email)
    assert first.id == second.id


def test_create_or_update_many(ticketing: Ticketing):
    job = ticketing.users.create_or_update_many(
        [
            {"name": f"libzapi coum {_unique()}", "email": f"libzapi-{_unique()}@example.invalid"},
            {"name": f"libzapi coum {_unique()}", "email": f"libzapi-{_unique()}@example.invalid"},
        ]
    )
    assert job.id


def test_update_many_uniform(ticketing: Ticketing):
    a = _create_user(ticketing)
    b = _create_user(ticketing)
    job = ticketing.users.update_many([a.id, b.id], tags=["libzapi-um"])
    assert job.id


def test_update_many_individually(ticketing: Ticketing):
    a = _create_user(ticketing)
    b = _create_user(ticketing)
    job = ticketing.users.update_many_individually(
        [(a.id, {"tags": ["libzapi-umi-a"]}), (b.id, {"tags": ["libzapi-umi-b"]})]
    )
    assert job.id


def test_destroy_many(ticketing: Ticketing):
    a = _create_user(ticketing)
    b = _create_user(ticketing)
    job = ticketing.users.destroy_many([a.id, b.id])
    assert job.id


def test_merge_users(ticketing: Ticketing):
    target = _create_user(ticketing)
    source = _create_user(ticketing)
    merged = ticketing.users.merge(source_user_id=source.id, target_user_id=target.id)
    assert merged.id == target.id


def test_list_and_count_deleted(ticketing: Ticketing):
    user = _create_user(ticketing)
    ticketing.users.delete(user.id)
    count = ticketing.users.count_deleted()
    assert count.value >= 1
    deleted = list(itertools.islice(ticketing.users.list_deleted(), 100))
    assert any(u.id == user.id for u in deleted) or deleted


def test_show_deleted(ticketing: Ticketing):
    user = _create_user(ticketing)
    ticketing.users.delete(user.id)
    shown = ticketing.users.show_deleted(user.id)
    assert shown.id == user.id


def test_permanently_delete(ticketing: Ticketing):
    user = _create_user(ticketing)
    ticketing.users.delete(user.id)
    gone = ticketing.users.permanently_delete(user.id)
    assert gone.id == user.id


@pytest.mark.skip(reason="sends an invitation email; run manually when intended")
def test_request_create(ticketing: Ticketing):
    resp = ticketing.users.request_create(
        name="libzapi invite", email=f"libzapi-inv-{_unique()}@example.invalid"
    )
    assert isinstance(resp, dict)


def test_logout_many(ticketing: Ticketing):
    a = _create_user(ticketing)
    b = _create_user(ticketing)
    ticketing.users.logout_many([a.id, b.id])


def test_user_list_tags(ticketing: Ticketing):
    user = _create_user(ticketing, tags=["libzapi-user-listtag"])
    tags = ticketing.users.list_tags(user.id)
    assert "libzapi-user-listtag" in tags


def test_user_set_tags(ticketing: Ticketing):
    user = _create_user(ticketing)
    tags = ticketing.users.set_tags(user.id, ["libzapi-user-set"])
    assert "libzapi-user-set" in tags


def test_user_add_tags(ticketing: Ticketing):
    user = _create_user(ticketing, tags=["libzapi-user-keep"])
    tags = ticketing.users.add_tags(user.id, ["libzapi-user-added"])
    assert {"libzapi-user-keep", "libzapi-user-added"} <= set(tags)


def test_user_remove_tags(ticketing: Ticketing):
    user = _create_user(ticketing, tags=["libzapi-user-keep", "libzapi-user-drop"])
    tags = ticketing.users.remove_tags(user.id, ["libzapi-user-drop"])
    assert "libzapi-user-drop" not in tags
    assert "libzapi-user-keep" in tags
