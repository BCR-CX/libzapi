from libzapi.application.commands.wfm.time_off_cmds import ImportTimeOffCmd


def to_payload_import(cmd: ImportTimeOffCmd) -> dict:
    entries = []
    for entry in cmd.data:
        item: dict = {
            "agentId": entry.agentId,
            "startTime": entry.startTime,
            "endTime": entry.endTime,
            "reasonId": entry.reasonId,
        }
        if entry.id is not None:
            item["id"] = entry.id
        if entry.note is not None:
            item["note"] = entry.note
        if entry.status is not None:
            item["status"] = entry.status
        if entry.timeOffType is not None:
            item["timeOffType"] = entry.timeOffType
        entries.append(item)
    return {"data": entries}
