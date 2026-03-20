from libzapi.application.commands.asset_management.asset_location_cmds import (
    CreateAssetLocationCmd,
    UpdateAssetLocationCmd,
)


def to_payload_create(cmd: CreateAssetLocationCmd) -> dict:
    payload: dict = {
        "name": cmd.name,
    }
    if cmd.external_id is not None:
        payload["external_id"] = cmd.external_id
    return {"location": payload}


def to_payload_update(cmd: UpdateAssetLocationCmd) -> dict:
    patch: dict = {}
    if cmd.name is not None:
        patch["name"] = cmd.name
    if cmd.external_id is not None:
        patch["external_id"] = cmd.external_id
    return {"location": patch}
