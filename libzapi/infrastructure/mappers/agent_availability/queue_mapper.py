from libzapi.application.commands.agent_availability.queue_cmds import CreateQueueCmd, UpdateQueueCmd


def to_payload_create(cmd: CreateQueueCmd) -> dict:
    payload: dict = {
        "name": cmd.name,
        "definition": cmd.definition,
        "priority": cmd.priority,
        "primary_groups": cmd.primary_groups,
    }
    if cmd.description is not None:
        payload["description"] = cmd.description
    if cmd.secondary_groups is not None:
        payload["secondary_groups"] = cmd.secondary_groups
    return {"queue": payload}


def to_payload_update(cmd: UpdateQueueCmd) -> dict:
    patch: dict = {}
    if cmd.name is not None:
        patch["name"] = cmd.name
    if cmd.description is not None:
        patch["description"] = cmd.description
    if cmd.definition is not None:
        patch["definition"] = cmd.definition
    if cmd.priority is not None:
        patch["priority"] = cmd.priority
    if cmd.primary_groups is not None:
        patch["primary_groups"] = cmd.primary_groups
    if cmd.secondary_groups is not None:
        patch["secondary_groups"] = cmd.secondary_groups
    return {"queue": patch}
