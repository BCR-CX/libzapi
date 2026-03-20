import pytest

from libzapi import AssetManagement


def test_list_and_get_asset_status(asset_management: AssetManagement):
    statuses = list(asset_management.asset_statuses.list_all())
    if not statuses:
        pytest.skip("No asset statuses found in the live API")
    status = asset_management.asset_statuses.get(statuses[0].id)
    assert status.id == statuses[0].id
