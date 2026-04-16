from libzapi.application.commands.voice.availability_cmds import UpdateAvailabilityCmd


def to_payload_update(cmd: UpdateAvailabilityCmd) -> dict:
    fields = ("agent_state", "call_status", "via")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"availability": patch}
