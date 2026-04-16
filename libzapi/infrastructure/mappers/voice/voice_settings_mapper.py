from libzapi.application.commands.voice.voice_settings_cmds import UpdateVoiceSettingsCmd


def to_payload_update(cmd: UpdateVoiceSettingsCmd) -> dict:
    fields = (
        "agent_confirmation_when_forwarding",
        "agent_wrap_up_after_calls",
        "maximum_queue_size",
        "maximum_queue_wait_time",
        "only_during_business_hours",
        "recordings_public",
    )
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"settings": patch}
