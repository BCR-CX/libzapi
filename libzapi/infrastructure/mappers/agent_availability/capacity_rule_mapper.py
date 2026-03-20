from libzapi.application.commands.agent_availability.capacity_rule_cmds import (
    CreateCapacityRuleCmd,
    UpdateCapacityRuleCmd,
)


def to_payload_create(cmd: CreateCapacityRuleCmd) -> dict:
    payload: dict = {
        "name": cmd.name,
        "capacities": cmd.capacities,
    }
    if cmd.description is not None:
        payload["description"] = cmd.description
    return payload


def to_payload_update(cmd: UpdateCapacityRuleCmd) -> dict:
    patch: dict = {}
    if cmd.name is not None:
        patch["name"] = cmd.name
    if cmd.description is not None:
        patch["description"] = cmd.description
    if cmd.capacities is not None:
        patch["capacities"] = cmd.capacities
    return patch
