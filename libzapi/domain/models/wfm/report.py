from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Grouping:
    key: str
    value: str


@dataclass(frozen=True, slots=True)
class Metric:
    key: str
    value: str
    type: str = ""


@dataclass(frozen=True, slots=True)
class ReportRow:
    groupings: list[Grouping] = field(default_factory=list)
    metrics: list[Metric] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        keys = "_".join(g.value for g in self.groupings)
        return LogicalKey("wfm_report_row", keys)
