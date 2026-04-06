from libzapi.application.commands.custom_data.permission_cmds import UpdatePermissionPolicyCmd


def to_payload_update(cmd: UpdatePermissionPolicyCmd) -> dict:
    fields = (
        "create",
        "read",
        "update",
        "delete",
        "create_rule_id",
        "read_rule_id",
        "update_rule_id",
        "delete_rule_id",
    )
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"permission_policy": patch}
