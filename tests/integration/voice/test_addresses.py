import pytest
from libzapi import Voice


def test_list_addresses(voice: Voice):
    addresses = list(voice.addresses.list_all())
    assert isinstance(addresses, list)


def test_list_and_get_address(voice: Voice):
    addresses = list(voice.addresses.list_all())
    if not addresses:
        pytest.skip("No addresses found")
    address = voice.addresses.get(addresses[0].id)
    assert address.id == addresses[0].id


def test_create_update_delete_address(voice: Voice):
    address = voice.addresses.create(
        city="São Paulo",
        country_code="BR",
        name="Integration Test Address",
        province="SP",
        street="Av. Paulista, 1000",
        zip="01310-100",
    )
    assert address.id is not None
    try:
        updated = voice.addresses.update(address.id, name="Updated Test Address")
        assert updated.name == "Updated Test Address"
    finally:
        voice.addresses.delete(address.id)
