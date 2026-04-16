from libzapi.application.commands.conversations.user_cmds import CreateUserCmd, UpdateUserCmd


def to_payload_create(cmd: CreateUserCmd) -> dict:
    payload: dict = {"externalId": cmd.externalId}
    if cmd.profile:
        payload["profile"] = cmd.profile
    if cmd.metadata:
        payload["metadata"] = cmd.metadata
    return payload


def to_payload_update(cmd: UpdateUserCmd) -> dict:
    fields = ("profile", "metadata")
    return {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
