import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def test_list_and_get_support_addresses(ticketing: Ticketing):
    addresses = list(ticketing.support_addresses.list())
    assert len(addresses) > 0
    address = ticketing.support_addresses.get(addresses[0].id)
    assert address.name == addresses[0].name


def test_create_update_delete_support_address(ticketing: Ticketing):
    suffix = _unique()
    address = ticketing.support_addresses.create(
        email=f"libzapi+{suffix}@libzapi.test",
        name=f"libzapi {suffix}",
    )
    try:
        assert address.id > 0
        updated = ticketing.support_addresses.update(
            address.id, name=f"libzapi updated {suffix}"
        )
        assert updated.name.startswith("libzapi updated")
    finally:
        ticketing.support_addresses.delete(address.id)
