import itertools
import uuid

import pytest

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _first_agent(ticketing: Ticketing):
    for u in itertools.islice(ticketing.users.list_all(), 200):
        if getattr(u, "role", None) in {"agent", "admin"}:
            return u
    pytest.skip("No agent user available for group-membership tests.")


def _fresh_group(ticketing: Ticketing):
    return ticketing.groups.create(
        name=f"libzapi gm {_unique()}",
        description="created by libzapi integration test",
    )


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.group_memberships.list_all(), 100))
    assert isinstance(items, list)


def test_list_by_user_and_group(ticketing: Ticketing):
    agent = _first_agent(ticketing)
    user_memberships = list(
        itertools.islice(ticketing.group_memberships.list_by_user(agent.id), 50)
    )
    assert isinstance(user_memberships, list)
    if user_memberships:
        gid = user_memberships[0].group_id
        group_memberships = list(
            itertools.islice(
                ticketing.group_memberships.list_by_group(gid), 50
            )
        )
        assert isinstance(group_memberships, list)


def test_list_assignable(ticketing: Ticketing):
    groups = list(itertools.islice(ticketing.groups.list_assignable(), 5))
    if not groups:
        pytest.skip("No assignable groups available.")
    items = list(
        itertools.islice(
            ticketing.group_memberships.list_assignable(groups[0].id), 50
        )
    )
    assert isinstance(items, list)


def test_create_delete(ticketing: Ticketing):
    agent = _first_agent(ticketing)
    group = _fresh_group(ticketing)
    try:
        membership = ticketing.group_memberships.create(
            user_id=agent.id, group_id=group.id
        )
        assert membership.id > 0
        assert membership.user_id == agent.id
        assert membership.group_id == group.id
        ticketing.group_memberships.delete(membership.id)
    finally:
        ticketing.groups.delete(group.id)


def test_get_by_id_and_for_user(ticketing: Ticketing):
    agent = _first_agent(ticketing)
    group = _fresh_group(ticketing)
    try:
        membership = ticketing.group_memberships.create(
            user_id=agent.id, group_id=group.id
        )
        fetched = ticketing.group_memberships.get_by_id(membership.id)
        assert fetched.id == membership.id
        fetched_for_user = ticketing.group_memberships.get_for_user(
            agent.id, membership.id
        )
        assert fetched_for_user.id == membership.id
        ticketing.group_memberships.delete(membership.id)
    finally:
        ticketing.groups.delete(group.id)


def test_create_many_and_destroy_many(ticketing: Ticketing):
    agent = _first_agent(ticketing)
    g1 = _fresh_group(ticketing)
    g2 = _fresh_group(ticketing)
    try:
        job = ticketing.group_memberships.create_many(
            [
                {"user_id": agent.id, "group_id": g1.id},
                {"user_id": agent.id, "group_id": g2.id},
            ]
        )
        assert job.id
    finally:
        ticketing.groups.delete(g1.id)
        ticketing.groups.delete(g2.id)
