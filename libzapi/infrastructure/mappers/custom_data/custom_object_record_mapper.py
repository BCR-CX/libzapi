from libzapi.application.commands.custom_data.custom_object_record_cmds import (
    BulkJobCmd,
    CreateCustomObjectRecordCmd,
    FilteredSearchCmd,
    UpdateCustomObjectRecordCmd,
)


def to_payload_create(cmd: CreateCustomObjectRecordCmd) -> dict:
    payload: dict = {
        "name": cmd.name,
        "custom_object_fields": cmd.custom_object_fields,
    }
    if cmd.external_id is not None:
        payload["external_id"] = cmd.external_id
    return {"custom_object_record": payload}


def to_payload_update(cmd: UpdateCustomObjectRecordCmd) -> dict:
    return {"custom_object_record": {"custom_object_fields": cmd.custom_object_fields}}


def to_payload_bulk_job(cmd: BulkJobCmd) -> dict:
    return {"job": {"action": cmd.action, "items": cmd.items}}


def to_payload_filtered_search(cmd: FilteredSearchCmd) -> dict:
    return {"filter": cmd.filter}
