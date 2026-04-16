from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateWebhookCmd:
    target: str
    triggers: list[str]
    includeFullUser: bool = False
    includeFullSource: bool = False


@dataclass(frozen=True, slots=True)
class UpdateWebhookCmd:
    target: str | None = None
    triggers: list[str] | None = None
    includeFullUser: bool | None = None
    includeFullSource: bool | None = None
