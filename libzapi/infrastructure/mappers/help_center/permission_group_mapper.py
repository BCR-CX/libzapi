from libzapi.application.commands.help_center.permission_group_cmds import (
    CreatePermissionGroupCmd,
    UpdatePermissionGroupCmd,
)


def to_payload_create(cmd: CreatePermissionGroupCmd) -> dict:
    payload: dict = {"name": cmd.name}
    if cmd.edit is not None:
        payload["edit"] = cmd.edit
    if cmd.publish is not None:
        payload["publish"] = cmd.publish
    return {"permission_group": payload}


def to_payload_update(cmd: UpdatePermissionGroupCmd) -> dict:
    fields = ("name", "edit", "publish")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"permission_group": patch}
