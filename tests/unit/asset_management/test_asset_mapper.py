from libzapi.application.commands.asset_management.asset_cmds import CreateAssetCmd, UpdateAssetCmd
from libzapi.application.commands.asset_management.asset_type_cmds import CreateAssetTypeCmd, UpdateAssetTypeCmd
from libzapi.application.commands.asset_management.asset_location_cmds import (
    CreateAssetLocationCmd,
    UpdateAssetLocationCmd,
)
from libzapi.infrastructure.mappers.asset_management.asset_mapper import (
    to_payload_create as asset_create,
    to_payload_update as asset_update,
)
from libzapi.infrastructure.mappers.asset_management.asset_type_mapper import (
    to_payload_create as type_create,
    to_payload_update as type_update,
)
from libzapi.infrastructure.mappers.asset_management.asset_location_mapper import (
    to_payload_create as location_create,
    to_payload_update as location_update,
)


# ── Asset mapper ────────────────────────────────────────────────────────


def test_asset_create_all_fields():
    cmd = CreateAssetCmd(
        name="Laptop",
        asset_type_id="type-1",
        status_id="status-1",
        asset_tag="TAG-001",
        location_id="loc-1",
        user_id=123,
        organization_id=456,
        serial_number="SN123",
        manufacturer="Dell",
        model="XPS 15",
        vendor="CDW",
        purchase_cost=1500.00,
        purchase_date="2024-01-01",
        warranty_expiration="2027-01-01",
        external_id="ext-1",
        notes="Dev laptop",
        custom_field_values={"color": "silver"},
    )
    result = asset_create(cmd)

    assert "asset" in result
    asset = result["asset"]
    assert asset["name"] == "Laptop"
    assert asset["asset_type_id"] == "type-1"
    assert asset["status_id"] == "status-1"
    assert asset["asset_tag"] == "TAG-001"
    assert asset["vendor"] == "CDW"
    assert asset["custom_field_values"] == {"color": "silver"}


def test_asset_create_minimal():
    cmd = CreateAssetCmd(name="Monitor", asset_type_id="type-2", status_id="status-1")
    result = asset_create(cmd)

    asset = result["asset"]
    assert asset["name"] == "Monitor"
    assert asset["asset_type_id"] == "type-2"
    assert asset["status_id"] == "status-1"
    assert "asset_tag" not in asset
    assert "vendor" not in asset
    assert "custom_field_values" not in asset


def test_asset_update_only_includes_non_none():
    cmd = UpdateAssetCmd(name="Updated Laptop", status_id="status-2")
    result = asset_update(cmd)
    assert result == {"asset": {"name": "Updated Laptop", "status_id": "status-2"}}


def test_asset_update_empty():
    cmd = UpdateAssetCmd()
    result = asset_update(cmd)
    assert result == {"asset": {}}


# ── Asset Type mapper ───────────────────────────────────────────────────


def test_asset_type_create_all_fields():
    cmd = CreateAssetTypeCmd(
        name="Laptop",
        parent_id="parent-1",
        description="Portable computers",
        external_id="ext-1",
        field_keys=["serial_number", "manufacturer"],
    )
    result = type_create(cmd)
    assert result == {
        "asset_type": {
            "name": "Laptop",
            "parent_id": "parent-1",
            "description": "Portable computers",
            "external_id": "ext-1",
            "field_keys": ["serial_number", "manufacturer"],
        }
    }


def test_asset_type_create_minimal():
    cmd = CreateAssetTypeCmd(name="Monitor", parent_id="parent-1")
    result = type_create(cmd)
    assert result == {"asset_type": {"name": "Monitor", "parent_id": "parent-1"}}


def test_asset_type_update_only_includes_non_none():
    cmd = UpdateAssetTypeCmd(description="Updated desc")
    result = type_update(cmd)
    assert result == {"asset_type": {"description": "Updated desc"}}


def test_asset_type_update_empty():
    cmd = UpdateAssetTypeCmd()
    result = type_update(cmd)
    assert result == {"asset_type": {}}


# ── Asset Location mapper ──────────────────────────────────────────────


def test_asset_location_create_all_fields():
    cmd = CreateAssetLocationCmd(name="NYC Office", external_id="ext-nyc")
    result = location_create(cmd)
    assert result == {"location": {"name": "NYC Office", "external_id": "ext-nyc"}}


def test_asset_location_create_minimal():
    cmd = CreateAssetLocationCmd(name="NYC Office")
    result = location_create(cmd)
    assert result == {"location": {"name": "NYC Office"}}


def test_asset_location_update_only_includes_non_none():
    cmd = UpdateAssetLocationCmd(name="SF Office")
    result = location_update(cmd)
    assert result == {"location": {"name": "SF Office"}}


def test_asset_location_update_empty():
    cmd = UpdateAssetLocationCmd()
    result = location_update(cmd)
    assert result == {"location": {}}
