from libzapi.application.commands.custom_data.custom_object_cmds import CreateCustomObjectCmd, UpdateCustomObjectCmd


def to_payload_create(cmd: CreateCustomObjectCmd) -> dict:
    payload: dict = {
        "key": cmd.key,
        "title": cmd.title,
        "title_pluralized": cmd.title_pluralized,
        "include_in_list_view": cmd.include_in_list_view,
    }
    if cmd.description:
        payload["description"] = cmd.description
    if cmd.allows_photos:
        payload["allows_photos"] = cmd.allows_photos
    if cmd.allows_attachments:
        payload["allows_attachments"] = cmd.allows_attachments
    return {"custom_object": payload}


def to_payload_update(cmd: UpdateCustomObjectCmd) -> dict:
    fields = ("title", "title_pluralized", "description", "include_in_list_view", "allows_photos", "allows_attachments")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"custom_object": patch}
