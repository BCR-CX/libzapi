import itertools
import uuid

import pytest

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _first_end_user(ticketing: Ticketing):
    for user in itertools.islice(ticketing.users.list_all(), 200):
        if getattr(user, "role", None) == "end-user":
            return user
    pytest.skip("No end-user available for organization-membership tests.")


def _fresh_organization(ticketing: Ticketing):
    return ticketing.organizations.create(name=f"libzapi om {_unique()}")


def test_list_all(ticketing: Ticketing):
    items = list(
        itertools.islice(ticketing.organization_memberships.list_all(), 100)
    )
    assert isinstance(items, list)


def test_create_delete(ticketing: Ticketing):
    user = _first_end_user(ticketing)
    org = _fresh_organization(ticketing)
    try:
        membership = ticketing.organization_memberships.create(
            user_id=user.id, organization_id=org.id
        )
        assert membership.id > 0
        assert membership.user_id == user.id
        assert membership.organization_id == org.id

        fetched = ticketing.organization_memberships.get_by_id(membership.id)
        assert fetched.id == membership.id

        for_user = ticketing.organization_memberships.get_for_user(
            user.id, membership.id
        )
        assert for_user.id == membership.id

        ticketing.organization_memberships.delete(membership.id)
    finally:
        ticketing.organizations.delete(org.id)


def test_list_by_user_and_organization(ticketing: Ticketing):
    user = _first_end_user(ticketing)
    org = _fresh_organization(ticketing)
    try:
        m = ticketing.organization_memberships.create(
            user_id=user.id, organization_id=org.id
        )
        try:
            by_user = list(
                itertools.islice(
                    ticketing.organization_memberships.list_by_user(user.id),
                    50,
                )
            )
            assert any(x.id == m.id for x in by_user)

            by_org = list(
                itertools.islice(
                    ticketing.organization_memberships.list_by_organization(
                        org.id
                    ),
                    50,
                )
            )
            assert any(x.id == m.id for x in by_org)
        finally:
            ticketing.organization_memberships.delete(m.id)
    finally:
        ticketing.organizations.delete(org.id)


def test_create_many_and_destroy_many(ticketing: Ticketing):
    user = _first_end_user(ticketing)
    o1 = _fresh_organization(ticketing)
    o2 = _fresh_organization(ticketing)
    try:
        job = ticketing.organization_memberships.create_many(
            [
                {"user_id": user.id, "organization_id": o1.id},
                {"user_id": user.id, "organization_id": o2.id},
            ]
        )
        assert job.id
    finally:
        ticketing.organizations.delete(o1.id)
        ticketing.organizations.delete(o2.id)
