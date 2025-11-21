from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from libzapi.domain.shared_objects.condition import AllAnyCondition


@dataclass(frozen=True, slots=True)
class SlaPolicyMetric:
    priority: str
    metric: str
    target: int
    business_hours: bool
    target_in_seconds: int


@dataclass(frozen=True, slots=True)
class SlaPolicy:
    url: str
    id: int
    title: str
    description: str
    position: int
    filter: AllAnyCondition
    policy_metrics: List[SlaPolicyMetric]
    created_at: datetime
    updated_at: datetime
    metric_settings: Optional[dict] = None