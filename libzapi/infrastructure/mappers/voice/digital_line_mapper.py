from libzapi.application.commands.voice.digital_line_cmds import CreateDigitalLineCmd, UpdateDigitalLineCmd


def to_payload_create(cmd: CreateDigitalLineCmd) -> dict:
    fields = ("nickname", "line_type", "brand_id", "default_group_id", "group_ids")
    payload = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"digital_line": payload}


def to_payload_update(cmd: UpdateDigitalLineCmd) -> dict:
    fields = ("nickname", "default_group_id", "group_ids", "recorded", "transcription", "schedule_id", "priority")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"digital_line": patch}
