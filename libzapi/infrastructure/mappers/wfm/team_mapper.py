from libzapi.application.commands.wfm.team_cmds import BulkAgentsCmd, CreateTeamCmd, UpdateTeamCmd


def to_payload_create(cmd: CreateTeamCmd) -> dict:
    return {
        "name": cmd.name,
        "description": cmd.description,
        "manager_id": cmd.manager_id,
        "agents_ids": cmd.agents_ids,
    }


def to_payload_update(cmd: UpdateTeamCmd) -> dict:
    fields = ("name", "description", "manager_id", "agents_ids")
    return {f: getattr(cmd, f) for f in fields if getattr(cmd, f) is not None}


def to_payload_bulk_agents(cmd: BulkAgentsCmd) -> dict:
    return {
        "agent_ids": cmd.agent_ids,
        "team_ids": cmd.team_ids,
    }
