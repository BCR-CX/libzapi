from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Via:
    channel: str
    source: dict
    rel: Optional[str] = None
