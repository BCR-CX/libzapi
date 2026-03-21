from libzapi.application.commands.help_center.article_comment_cmds import (
    CreateArticleCommentCmd,
    UpdateArticleCommentCmd,
)


def to_payload_create(cmd: CreateArticleCommentCmd) -> dict:
    payload: dict = {"body": cmd.body, "notify_subscribers": cmd.notify_subscribers}
    if cmd.locale is not None:
        payload["locale"] = cmd.locale
    if cmd.author_id is not None:
        payload["author_id"] = cmd.author_id
    return {"comment": payload}


def to_payload_update(cmd: UpdateArticleCommentCmd) -> dict:
    patch: dict = {}
    if cmd.body is not None:
        patch["body"] = cmd.body
    return {"comment": patch}
