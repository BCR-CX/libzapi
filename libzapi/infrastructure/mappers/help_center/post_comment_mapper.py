from libzapi.application.commands.help_center.post_comment_cmds import CreatePostCommentCmd, UpdatePostCommentCmd


def to_payload_create(cmd: CreatePostCommentCmd) -> dict:
    return {"comment": {"body": cmd.body, "notify_subscribers": cmd.notify_subscribers}}


def to_payload_update(cmd: UpdatePostCommentCmd) -> dict:
    fields = ("body", "official")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"comment": patch}
