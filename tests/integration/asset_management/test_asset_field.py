import pytest

from libzapi import AssetManagement


def test_list_and_get_asset_field(asset_management: AssetManagement):
    asset_types = list(asset_management.asset_types.list_all())
    if not asset_types:
        pytest.skip("No asset types found in the live API")
    fields = list(asset_management.asset_fields.list_all(asset_types[0].id))
    if not fields:
        pytest.skip("No asset fields found in the live API")
    field = asset_management.asset_fields.get(asset_types[0].id, fields[0].id)
    assert field.id == fields[0].id
