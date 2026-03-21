from libzapi.application.commands.help_center.article_label_cmds import CreateArticleLabelCmd


def to_payload_create(cmd: CreateArticleLabelCmd) -> dict:
    return {"label": {"name": cmd.name}}
