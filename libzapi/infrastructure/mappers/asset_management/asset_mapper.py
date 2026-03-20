from libzapi.application.commands.asset_management.asset_cmds import CreateAssetCmd, UpdateAssetCmd


def to_payload_create(cmd: CreateAssetCmd) -> dict:
    payload: dict = {
        "name": cmd.name,
        "asset_type_id": cmd.asset_type_id,
        "status_id": cmd.status_id,
    }
    if cmd.asset_tag is not None:
        payload["asset_tag"] = cmd.asset_tag
    if cmd.location_id is not None:
        payload["location_id"] = cmd.location_id
    if cmd.user_id is not None:
        payload["user_id"] = cmd.user_id
    if cmd.organization_id is not None:
        payload["organization_id"] = cmd.organization_id
    if cmd.serial_number is not None:
        payload["serial_number"] = cmd.serial_number
    if cmd.manufacturer is not None:
        payload["manufacturer"] = cmd.manufacturer
    if cmd.model is not None:
        payload["model"] = cmd.model
    if cmd.vendor is not None:
        payload["vendor"] = cmd.vendor
    if cmd.purchase_cost is not None:
        payload["purchase_cost"] = cmd.purchase_cost
    if cmd.purchase_date is not None:
        payload["purchase_date"] = cmd.purchase_date
    if cmd.warranty_expiration is not None:
        payload["warranty_expiration"] = cmd.warranty_expiration
    if cmd.external_id is not None:
        payload["external_id"] = cmd.external_id
    if cmd.notes is not None:
        payload["notes"] = cmd.notes
    if cmd.custom_field_values is not None:
        payload["custom_field_values"] = cmd.custom_field_values
    return {"asset": payload}


def to_payload_update(cmd: UpdateAssetCmd) -> dict:
    patch: dict = {}
    if cmd.name is not None:
        patch["name"] = cmd.name
    if cmd.status_id is not None:
        patch["status_id"] = cmd.status_id
    if cmd.asset_tag is not None:
        patch["asset_tag"] = cmd.asset_tag
    if cmd.location_id is not None:
        patch["location_id"] = cmd.location_id
    if cmd.user_id is not None:
        patch["user_id"] = cmd.user_id
    if cmd.organization_id is not None:
        patch["organization_id"] = cmd.organization_id
    if cmd.serial_number is not None:
        patch["serial_number"] = cmd.serial_number
    if cmd.manufacturer is not None:
        patch["manufacturer"] = cmd.manufacturer
    if cmd.model is not None:
        patch["model"] = cmd.model
    if cmd.vendor is not None:
        patch["vendor"] = cmd.vendor
    if cmd.purchase_cost is not None:
        patch["purchase_cost"] = cmd.purchase_cost
    if cmd.purchase_date is not None:
        patch["purchase_date"] = cmd.purchase_date
    if cmd.warranty_expiration is not None:
        patch["warranty_expiration"] = cmd.warranty_expiration
    if cmd.external_id is not None:
        patch["external_id"] = cmd.external_id
    if cmd.notes is not None:
        patch["notes"] = cmd.notes
    if cmd.custom_field_values is not None:
        patch["custom_field_values"] = cmd.custom_field_values
    return {"asset": patch}
