from libzapi.application.commands.help_center.translation_cmds import CreateTranslationCmd, UpdateTranslationCmd


def to_payload_create(cmd: CreateTranslationCmd) -> dict:
    return {
        "translation": {
            "locale": cmd.locale,
            "title": cmd.title,
            "body": cmd.body,
            "draft": cmd.draft,
            "outdated": cmd.outdated,
        }
    }


def to_payload_update(cmd: UpdateTranslationCmd) -> dict:
    fields = ("title", "body", "draft", "outdated")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"translation": patch}
