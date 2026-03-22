from libzapi.application.commands.wfm.shift_cmds import FetchShiftsCmd


def to_payload_fetch(cmd: FetchShiftsCmd) -> dict:
    payload: dict = {
        "startDate": cmd.startDate,
        "endDate": cmd.endDate,
    }
    if cmd.agentIds is not None:
        payload["agentIds"] = cmd.agentIds
    if cmd.published is not None:
        payload["published"] = cmd.published
    if cmd.page != 1:
        payload["page"] = cmd.page
    return payload
