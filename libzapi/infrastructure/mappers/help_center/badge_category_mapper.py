from libzapi.application.commands.help_center.badge_category_cmds import CreateBadgeCategoryCmd


def to_payload_create(cmd: CreateBadgeCategoryCmd) -> dict:
    return {"badge_category": {"brand_id": cmd.brand_id, "name": cmd.name, "slug": cmd.slug}}
