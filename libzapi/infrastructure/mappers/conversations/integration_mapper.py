from libzapi.application.commands.conversations.integration_cmds import CreateIntegrationCmd, UpdateIntegrationCmd


def to_payload_create(cmd: CreateIntegrationCmd) -> dict:
    payload: dict = {"type": cmd.type}
    if cmd.displayName:
        payload["displayName"] = cmd.displayName
    if cmd.extra:
        payload.update(cmd.extra)
    return payload


def to_payload_update(cmd: UpdateIntegrationCmd) -> dict:
    payload: dict = {}
    if cmd.displayName is not None:
        payload["displayName"] = cmd.displayName
    if cmd.extra is not None:
        payload.update(cmd.extra)
    return payload
