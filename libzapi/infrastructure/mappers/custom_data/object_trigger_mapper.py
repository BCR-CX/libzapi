from libzapi.application.commands.custom_data.object_trigger_cmds import (
    CreateObjectTriggerCmd,
    UpdateManyTriggersCmd,
    UpdateObjectTriggerCmd,
)


def to_payload_create(cmd: CreateObjectTriggerCmd) -> dict:
    payload: dict = {
        "title": cmd.title,
        "conditions": cmd.conditions,
        "actions": cmd.actions,
        "active": cmd.active,
    }
    if cmd.description:
        payload["description"] = cmd.description
    return {"trigger": payload}


def to_payload_update(cmd: UpdateObjectTriggerCmd) -> dict:
    fields = ("title", "conditions", "actions", "active", "description")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"trigger": patch}


def to_payload_update_many(cmd: UpdateManyTriggersCmd) -> dict:
    return {"triggers": cmd.triggers}
