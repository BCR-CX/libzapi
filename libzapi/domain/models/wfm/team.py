from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Team:
    id: str
    name: str
    description: str = ""
    manager_id: int | None = None
    agents_ids: list[str] = field(default_factory=list)
    is_deleted: bool = False
    deleted_at: str | None = None
    tymeshift_account_id: int | None = None

    @property
    def logical_key(self) -> LogicalKey:
        base = self.name.lower().replace(" ", "_")
        return LogicalKey("wfm_team", base)


@dataclass(frozen=True, slots=True)
class BulkAgentsResult:
    status: str = ""
    affected_teams: list[str] = field(default_factory=list)
