from libzapi.application.commands.help_center.topic_cmds import CreateTopicCmd, UpdateTopicCmd


def to_payload_create(cmd: CreateTopicCmd) -> dict:
    payload: dict = {"name": cmd.name, "description": cmd.description, "position": cmd.position}
    if cmd.manageable_by is not None:
        payload["manageable_by"] = cmd.manageable_by
    if cmd.user_segment_id is not None:
        payload["user_segment_id"] = cmd.user_segment_id
    return {"topic": payload}


def to_payload_update(cmd: UpdateTopicCmd) -> dict:
    fields = ("name", "description", "position", "manageable_by", "user_segment_id")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"topic": patch}
