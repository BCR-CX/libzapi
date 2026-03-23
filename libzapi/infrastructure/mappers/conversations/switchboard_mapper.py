from libzapi.application.commands.conversations.switchboard_cmds import (
    CreateSwitchboardCmd,
    CreateSwitchboardIntegrationCmd,
    UpdateSwitchboardCmd,
    UpdateSwitchboardIntegrationCmd,
)


def to_payload_create_switchboard(cmd: CreateSwitchboardCmd) -> dict:
    return {"enabled": cmd.enabled}


def to_payload_update_switchboard(cmd: UpdateSwitchboardCmd) -> dict:
    fields = ("enabled", "defaultSwitchboardIntegrationId")
    return {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}


def to_payload_create_switchboard_integration(cmd: CreateSwitchboardIntegrationCmd) -> dict:
    payload: dict = {
        "name": cmd.name,
        "integrationId": cmd.integrationId,
    }
    if cmd.integrationType:
        payload["integrationType"] = cmd.integrationType
    if cmd.deliverStandbyEvents:
        payload["deliverStandbyEvents"] = cmd.deliverStandbyEvents
    return payload


def to_payload_update_switchboard_integration(cmd: UpdateSwitchboardIntegrationCmd) -> dict:
    fields = ("name", "deliverStandbyEvents", "nextSwitchboardIntegrationId", "messageHistoryCount")
    return {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}
