from libzapi.application.commands.custom_data.permission_cmds import CreateAccessRuleCmd, UpdateAccessRuleCmd


def to_payload_create(cmd: CreateAccessRuleCmd) -> dict:
    payload: dict = {"name": cmd.name}
    if cmd.conditions:
        payload["conditions"] = cmd.conditions
    return {"access_rule": payload}


def to_payload_update(cmd: UpdateAccessRuleCmd) -> dict:
    fields = ("name", "conditions")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"access_rule": patch}
