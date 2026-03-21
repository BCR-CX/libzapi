from libzapi.application.commands.help_center.article_cmds import CreateArticleCmd, UpdateArticleCmd


def to_payload_create(cmd: CreateArticleCmd) -> dict:
    payload: dict = {
        "title": cmd.title,
        "body": cmd.body,
        "locale": cmd.locale,
        "comments_disabled": cmd.comments_disabled,
        "promoted": cmd.promoted,
        "position": cmd.position,
    }
    if cmd.author_id is not None:
        payload["author_id"] = cmd.author_id
    if cmd.permission_group_id is not None:
        payload["permission_group_id"] = cmd.permission_group_id
    if cmd.user_segment_id is not None:
        payload["user_segment_id"] = cmd.user_segment_id
    if cmd.content_tag_ids is not None:
        payload["content_tag_ids"] = cmd.content_tag_ids
    if cmd.label_names is not None:
        payload["label_names"] = cmd.label_names
    return {"article": payload}


def to_payload_update(cmd: UpdateArticleCmd) -> dict:
    fields = (
        "title",
        "body",
        "locale",
        "author_id",
        "comments_disabled",
        "promoted",
        "position",
        "permission_group_id",
        "user_segment_id",
        "content_tag_ids",
        "label_names",
    )
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"article": patch}
