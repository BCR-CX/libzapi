import uuid

import pytest

from libzapi import AssetManagement
from libzapi.application.commands.asset_management.asset_location_cmds import (
    CreateAssetLocationCmd,
    UpdateAssetLocationCmd,
)


def test_list_and_get_asset_location(asset_management: AssetManagement):
    locations = list(asset_management.asset_locations.list_all())
    if not locations:
        pytest.skip("No asset locations found in the live API")
    location = asset_management.asset_locations.get(locations[0].id)
    assert location.id == locations[0].id


def test_create_update_delete_asset_location(asset_management: AssetManagement):
    random_id = str(uuid.uuid4())[:8]

    new_location = asset_management.asset_locations.create(
        CreateAssetLocationCmd(
            name=f"Test Location {random_id}",
        )
    )
    assert new_location.id is not None, "Expected the created location to have an ID"

    try:
        updated_location = asset_management.asset_locations.update(
            new_location.id,
            UpdateAssetLocationCmd(name=f"Updated Location {random_id}"),
        )
        assert updated_location.name == f"Updated Location {random_id}", "Expected the location name to be updated"

        fetched_location = asset_management.asset_locations.get(new_location.id)
        assert fetched_location.id == new_location.id, "Expected to fetch the same location by ID"

    finally:
        asset_management.asset_locations.delete(new_location.id)
