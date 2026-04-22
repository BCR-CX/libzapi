import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _fresh_end_user(ticketing: Ticketing):
    return ticketing.users.create(
        name=f"libzapi identity test {_unique()}",
        email=f"libzapi_{_unique()}@example.test",
        role="end-user",
    )


def test_list_for_user(ticketing: Ticketing):
    user = _fresh_end_user(ticketing)
    try:
        identities = list(ticketing.user_identities.list_for_user(user.id))
        assert isinstance(identities, list)
        assert any(i.type == "email" for i in identities)
    finally:
        ticketing.users.delete(user.id)


def test_create_get_delete_phone_identity(ticketing: Ticketing):
    user = _fresh_end_user(ticketing)
    try:
        created = ticketing.user_identities.create(
            user_id=user.id,
            type="phone_number",
            value=f"+1555{_unique()[:7]}",
            verified=True,
        )
        assert created.id > 0
        assert created.verified is True

        fetched = ticketing.user_identities.get_by_id(user.id, created.id)
        assert fetched.id == created.id

        ticketing.user_identities.delete(user.id, created.id)
    finally:
        ticketing.users.delete(user.id)


def test_update_identity(ticketing: Ticketing):
    user = _fresh_end_user(ticketing)
    try:
        created = ticketing.user_identities.create(
            user_id=user.id,
            type="email",
            value=f"extra_{_unique()}@example.test",
            verified=True,
        )
        try:
            new_value = f"renamed_{_unique()}@example.test"
            updated = ticketing.user_identities.update(
                user.id, created.id, value=new_value
            )
            assert updated.value == new_value
        finally:
            ticketing.user_identities.delete(user.id, created.id)
    finally:
        ticketing.users.delete(user.id)


def test_make_primary_promotes_identity(ticketing: Ticketing):
    user = _fresh_end_user(ticketing)
    try:
        created = ticketing.user_identities.create(
            user_id=user.id,
            type="email",
            value=f"primary_{_unique()}@example.test",
            verified=True,
        )
        try:
            identities = ticketing.user_identities.make_primary(
                user.id, created.id
            )
            assert any(i.id == created.id and i.primary for i in identities)
        finally:
            # promoted identity cannot be deleted if it's the sole primary.
            # Restore original primary by deleting user (handled in outer finally).
            pass
    finally:
        ticketing.users.delete(user.id)
