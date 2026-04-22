from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True, slots=True)
class ZendeskIPs:
    project: Optional[str] = None
    egress_ips: List[str] = field(default_factory=list)
    ingress_ips: List[str] = field(default_factory=list)
    app_id: Optional[str] = None
