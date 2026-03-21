from libzapi.application.commands.help_center.content_tag_cmds import CreateContentTagCmd, UpdateContentTagCmd


def to_payload_create(cmd: CreateContentTagCmd) -> dict:
    return {"content_tag": {"name": cmd.name}}


def to_payload_update(cmd: UpdateContentTagCmd) -> dict:
    patch: dict = {}
    if cmd.name is not None:
        patch["name"] = cmd.name
    return {"content_tag": patch}
