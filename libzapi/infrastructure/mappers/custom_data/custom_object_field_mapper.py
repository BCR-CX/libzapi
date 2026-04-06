from libzapi.application.commands.custom_data.custom_object_field_cmds import (
    CreateCustomObjectFieldCmd,
    UpdateCustomObjectFieldCmd,
)


def to_payload_create(cmd: CreateCustomObjectFieldCmd) -> dict:
    payload: dict = {
        "type": cmd.type,
        "key": cmd.key,
        "title": cmd.title,
    }
    if cmd.description:
        payload["description"] = cmd.description
    if cmd.active is not True:
        payload["active"] = cmd.active
    if cmd.position:
        payload["position"] = cmd.position
    if cmd.regexp_for_validation is not None:
        payload["regexp_for_validation"] = cmd.regexp_for_validation
    if cmd.custom_field_options is not None:
        payload["custom_field_options"] = cmd.custom_field_options
    if cmd.relationship_target_type is not None:
        payload["relationship_target_type"] = cmd.relationship_target_type
    if cmd.relationship_filter is not None:
        payload["relationship_filter"] = cmd.relationship_filter
    if cmd.tag is not None:
        payload["tag"] = cmd.tag
    return {"custom_object_field": payload}


def to_payload_update(cmd: UpdateCustomObjectFieldCmd) -> dict:
    fields = ("title", "description", "active", "position", "custom_field_options")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"custom_object_field": patch}


def to_payload_reorder(field_ids: list[int]) -> dict:
    return {"field_ids": field_ids}
