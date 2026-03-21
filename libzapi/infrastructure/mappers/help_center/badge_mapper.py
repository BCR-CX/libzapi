from libzapi.application.commands.help_center.badge_cmds import CreateBadgeCmd, UpdateBadgeCmd


def to_payload_create(cmd: CreateBadgeCmd) -> dict:
    return {"badge": {"badge_category_id": cmd.badge_category_id, "name": cmd.name, "description": cmd.description}}


def to_payload_update(cmd: UpdateBadgeCmd) -> dict:
    fields = ("name", "description", "badge_category_id")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"badge": patch}
