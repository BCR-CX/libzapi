from libzapi.application.commands.conversations.switchboard_action_cmds import OfferControlCmd, PassControlCmd


def to_payload_pass_control(cmd: PassControlCmd) -> dict:
    payload: dict = {"switchboardIntegration": cmd.switchboardIntegration}
    if cmd.metadata:
        payload["metadata"] = cmd.metadata
    return payload


def to_payload_offer_control(cmd: OfferControlCmd) -> dict:
    payload: dict = {"switchboardIntegration": cmd.switchboardIntegration}
    if cmd.metadata:
        payload["metadata"] = cmd.metadata
    return payload
