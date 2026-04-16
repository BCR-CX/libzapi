from libzapi.application.commands.conversations.app_cmds import CreateAppCmd, UpdateAppCmd


def to_payload_create(cmd: CreateAppCmd) -> dict:
    payload: dict = {"displayName": cmd.displayName}
    if cmd.metadata:
        payload["metadata"] = cmd.metadata
    if cmd.settings:
        payload["settings"] = cmd.settings
    return payload


def to_payload_update(cmd: UpdateAppCmd) -> dict:
    fields = ("displayName", "metadata", "settings")
    return {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
