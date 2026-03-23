from libzapi.application.commands.conversations.message_cmds import PostMessageCmd


def to_payload_create(cmd: PostMessageCmd) -> dict:
    payload: dict = {"author": cmd.author, "content": cmd.content}
    if cmd.metadata:
        payload["metadata"] = cmd.metadata
    return payload
