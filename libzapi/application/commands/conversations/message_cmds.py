from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PostMessageCmd:
    author: dict
    content: dict
    metadata: dict | None = None
