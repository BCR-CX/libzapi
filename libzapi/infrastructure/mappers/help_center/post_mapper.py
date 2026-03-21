from libzapi.application.commands.help_center.post_cmds import CreatePostCmd, UpdatePostCmd


def to_payload_create(cmd: CreatePostCmd) -> dict:
    payload: dict = {
        "title": cmd.title,
        "details": cmd.details,
        "topic_id": cmd.topic_id,
        "notify_subscribers": cmd.notify_subscribers,
    }
    if cmd.content_tag_ids is not None:
        payload["content_tag_ids"] = cmd.content_tag_ids
    return {"post": payload}


def to_payload_update(cmd: UpdatePostCmd) -> dict:
    fields = ("title", "details", "topic_id", "content_tag_ids")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"post": patch}
