import itertools
import uuid

import pytest

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_brand(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        name=f"libzapi brand {suffix}",
        subdomain=f"libzapi-{suffix}",
    )
    defaults.update(overrides)
    return ticketing.brands.create(**defaults)


def test_list_and_get(ticketing: Ticketing):
    brands = list(itertools.islice(ticketing.brands.list(), 50))
    assert len(brands) > 0
    brand = ticketing.brands.get(brands[0].id)
    assert brand.id == brands[0].id


def test_create_update_delete(ticketing: Ticketing):
    try:
        brand = _create_brand(ticketing, signature_template="hello")
    except Exception as e:
        pytest.skip(f"Cannot create brand on this tenant: {e}")
    try:
        assert brand.id > 0
        updated = ticketing.brands.update(
            brand.id, signature_template="updated by libzapi"
        )
        assert updated.signature_template == "updated by libzapi"
    finally:
        ticketing.brands.delete(brand.id)


def test_check_host_mapping(ticketing: Ticketing):
    result = ticketing.brands.check_host_mapping(
        host_mapping=f"help-{_unique()}.invalid.example", subdomain=f"libzapi-{_unique()}"
    )
    assert isinstance(result, dict)
