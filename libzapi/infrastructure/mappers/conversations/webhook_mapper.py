from libzapi.application.commands.conversations.webhook_cmds import CreateWebhookCmd, UpdateWebhookCmd


def to_payload_create(cmd: CreateWebhookCmd) -> dict:
    payload: dict = {
        "target": cmd.target,
        "triggers": cmd.triggers,
    }
    if cmd.includeFullUser:
        payload["includeFullUser"] = cmd.includeFullUser
    if cmd.includeFullSource:
        payload["includeFullSource"] = cmd.includeFullSource
    return payload


def to_payload_update(cmd: UpdateWebhookCmd) -> dict:
    fields = ("target", "triggers", "includeFullUser", "includeFullSource")
    return {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
