from __future__ import annotations

from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Author:
    type: str = ""
    userId: str = ""
    userExternalId: str = ""
    displayName: str = ""
    avatarUrl: str = ""


@dataclass(frozen=True, slots=True)
class Source:
    type: str = ""
    integrationId: str = ""
    originalMessageId: str = ""
    originalMessageTimestamp: str = ""


@dataclass(frozen=True, slots=True)
class Message:
    id: str
    received: str = ""
    deleted: bool = False
    author: Author | None = None
    content: dict | None = None
    source: Source | None = None
    metadata: dict | None = None
    quotedMessage: dict | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("message", self.id)
