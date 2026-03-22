from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateTeamCmd:
    name: str
    description: str
    manager_id: int
    agents_ids: list[str]


@dataclass(frozen=True, slots=True)
class UpdateTeamCmd:
    name: str | None = None
    description: str | None = None
    manager_id: int | None = None
    agents_ids: list[str] | None = None


@dataclass(frozen=True, slots=True)
class BulkAgentsCmd:
    agent_ids: list[str]
    team_ids: list[str]
