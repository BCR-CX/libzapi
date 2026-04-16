from libzapi.application.commands.voice.callback_request_cmds import CreateCallbackRequestCmd


def to_payload_create(cmd: CreateCallbackRequestCmd) -> dict:
    payload: dict = {
        "phone_number_id": cmd.phone_number_id,
        "requester_phone_number": cmd.requester_phone_number,
    }
    if cmd.group_ids:
        payload["group_ids"] = cmd.group_ids
    return payload
