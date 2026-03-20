import uuid

import pytest

from libzapi import AssetManagement
from libzapi.application.commands.asset_management.asset_type_cmds import CreateAssetTypeCmd, UpdateAssetTypeCmd


def test_list_and_get_asset_type(asset_management: AssetManagement):
    asset_types = list(asset_management.asset_types.list_all())
    if not asset_types:
        pytest.skip("No asset types found in the live API")
    asset_type = asset_management.asset_types.get(asset_types[0].id)
    assert asset_type.id == asset_types[0].id


def test_create_update_delete_asset_type(asset_management: AssetManagement):
    # Need an existing asset type as parent
    asset_types = list(asset_management.asset_types.list_all())
    if not asset_types:
        pytest.skip("No asset types found — cannot create a child type")

    random_id = str(uuid.uuid4())[:8]
    new_type = asset_management.asset_types.create(
        CreateAssetTypeCmd(
            name=f"Test Type {random_id}",
            parent_id=asset_types[0].id,
            description="Created for testing purposes",
        )
    )
    assert new_type.id is not None, "Expected the created asset type to have an ID"

    try:
        updated_type = asset_management.asset_types.update(
            new_type.id,
            UpdateAssetTypeCmd(description=f"Updated description {random_id}"),
        )
        assert "Updated description" in updated_type.description, "Expected the description to be updated"

        fetched_type = asset_management.asset_types.get(new_type.id)
        assert fetched_type.id == new_type.id, "Expected to fetch the same asset type by ID"

    finally:
        asset_management.asset_types.delete(new_type.id)
