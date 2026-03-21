from libzapi.application.commands.help_center.badge_assignment_cmds import CreateBadgeAssignmentCmd


def to_payload_create(cmd: CreateBadgeAssignmentCmd) -> dict:
    return {"badge_assignment": {"badge_id": cmd.badge_id, "user_id": cmd.user_id}}
