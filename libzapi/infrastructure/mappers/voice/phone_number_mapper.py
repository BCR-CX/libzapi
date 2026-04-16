from libzapi.application.commands.voice.phone_number_cmds import CreatePhoneNumberCmd, UpdatePhoneNumberCmd


def to_payload_create(cmd: CreatePhoneNumberCmd) -> dict:
    payload: dict = {"token": cmd.token}
    if cmd.nickname:
        payload["nickname"] = cmd.nickname
    if cmd.address_sid is not None:
        payload["address_sid"] = cmd.address_sid
    return {"phone_number": payload}


def to_payload_update(cmd: UpdatePhoneNumberCmd) -> dict:
    fields = (
        "nickname",
        "default_group_id",
        "group_ids",
        "priority",
        "outbound_enabled",
        "voice_enabled",
        "sms_enabled",
        "recorded",
        "transcription",
        "greeting_ids",
        "schedule_id",
        "ivr_id",
        "call_recording_consent",
        "failover_number",
    )
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"phone_number": patch}
