import uuid

import pytest

from libzapi import AssetManagement
from libzapi.application.commands.asset_management.asset_cmds import CreateAssetCmd, UpdateAssetCmd


def test_list_and_get_asset(asset_management: AssetManagement):
    assets = list(asset_management.assets.list_all())
    if not assets:
        pytest.skip("No assets found in the live API")
    asset = asset_management.assets.get(assets[0].id)
    assert asset.id == assets[0].id


def test_create_update_delete_asset(asset_management: AssetManagement):
    # We need an asset type and a status to create an asset
    asset_types = list(asset_management.asset_types.list_all())
    if not asset_types:
        pytest.skip("No asset types found — cannot create an asset")

    statuses = list(asset_management.asset_statuses.list_all())
    if not statuses:
        pytest.skip("No asset statuses found — cannot create an asset")

    random_id = str(uuid.uuid4())[:8]
    new_asset = asset_management.assets.create(
        CreateAssetCmd(
            name=f"Test Asset {random_id}",
            asset_type_id=asset_types[0].id,
            status_id=statuses[0].id,
            serial_number=f"SN-{random_id}",
        )
    )
    assert new_asset.id is not None, "Expected the created asset to have an ID"

    try:
        updated_asset = asset_management.assets.update(
            new_asset.id,
            UpdateAssetCmd(name=f"Updated Asset {random_id}"),
        )
        assert updated_asset.name == f"Updated Asset {random_id}", "Expected the asset name to be updated"

        fetched_asset = asset_management.assets.get(new_asset.id)
        assert fetched_asset.id == new_asset.id, "Expected to fetch the same asset by ID"

    finally:
        asset_management.assets.delete(new_asset.id)
