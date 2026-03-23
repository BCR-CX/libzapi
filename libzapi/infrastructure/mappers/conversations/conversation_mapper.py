from libzapi.application.commands.conversations.conversation_cmds import CreateConversationCmd, UpdateConversationCmd


def to_payload_create(cmd: CreateConversationCmd) -> dict:
    payload: dict = {"type": cmd.type}
    if cmd.displayName:
        payload["displayName"] = cmd.displayName
    if cmd.description:
        payload["description"] = cmd.description
    if cmd.iconUrl:
        payload["iconUrl"] = cmd.iconUrl
    if cmd.metadata:
        payload["metadata"] = cmd.metadata
    if cmd.participants:
        payload["participants"] = cmd.participants
    return payload


def to_payload_update(cmd: UpdateConversationCmd) -> dict:
    fields = ("displayName", "description", "iconUrl", "metadata")
    return {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
