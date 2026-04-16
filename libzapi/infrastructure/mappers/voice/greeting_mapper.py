from libzapi.application.commands.voice.greeting_cmds import CreateGreetingCmd, UpdateGreetingCmd


def to_payload_create(cmd: CreateGreetingCmd) -> dict:
    payload: dict = {"category_id": cmd.category_id, "name": cmd.name}
    if cmd.audio_name:
        payload["audio_name"] = cmd.audio_name
    return {"greeting": payload}


def to_payload_update(cmd: UpdateGreetingCmd) -> dict:
    fields = ("name",)
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"greeting": patch}
