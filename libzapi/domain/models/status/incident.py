from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Incident:
    id: str
    title: str
    impact: str | None = None
    started_at: str | None = None
    resolved_at: str | None = None
    status: str | None = None
    outage: bool = False
    degradation: bool = False
    postmortem: str | None = None
    maintenance_start_time: str | None = None
    maintenance_end_time: str | None = None
    maintenance_article: str | None = None
    updates: list[dict] = field(default_factory=list)
    services: list[dict] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("incident", self.id)
