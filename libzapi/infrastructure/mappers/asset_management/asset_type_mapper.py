from libzapi.application.commands.asset_management.asset_type_cmds import CreateAssetTypeCmd, UpdateAssetTypeCmd


def to_payload_create(cmd: CreateAssetTypeCmd) -> dict:
    payload: dict = {
        "name": cmd.name,
        "parent_id": cmd.parent_id,
    }
    if cmd.description is not None:
        payload["description"] = cmd.description
    if cmd.external_id is not None:
        payload["external_id"] = cmd.external_id
    if cmd.field_keys is not None:
        payload["field_keys"] = cmd.field_keys
    return {"asset_type": payload}


def to_payload_update(cmd: UpdateAssetTypeCmd) -> dict:
    patch: dict = {}
    if cmd.description is not None:
        patch["description"] = cmd.description
    if cmd.external_id is not None:
        patch["external_id"] = cmd.external_id
    if cmd.field_keys is not None:
        patch["field_keys"] = cmd.field_keys
    return {"asset_type": patch}
