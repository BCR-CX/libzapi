from libzapi.application.commands.voice.address_cmds import CreateAddressCmd, UpdateAddressCmd


def to_payload_create(cmd: CreateAddressCmd) -> dict:
    payload: dict = {
        "city": cmd.city,
        "country_code": cmd.country_code,
        "name": cmd.name,
        "province": cmd.province,
        "street": cmd.street,
        "zip": cmd.zip,
    }
    if cmd.state:
        payload["state"] = cmd.state
    if cmd.provider_reference:
        payload["provider_reference"] = cmd.provider_reference
    return {"address": payload}


def to_payload_update(cmd: UpdateAddressCmd) -> dict:
    fields = ("city", "country_code", "name", "province", "street", "zip", "state")
    patch = {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
    return {"address": patch}
