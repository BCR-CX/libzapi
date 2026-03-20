from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class JobStatus:
    id: str
    status: str
    message: str | None = None
    progress: int | None = None
    total: int | None = None
    results: list[dict] = field(default_factory=list)
    url: str | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("job_status", self.id)
