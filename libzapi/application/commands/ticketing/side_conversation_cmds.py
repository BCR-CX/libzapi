from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True, slots=True)
class SideConversationMessageCmd:
    body: str
    subject: Optional[str] = None
    to: List[dict] = field(default_factory=list)
    from_: Optional[dict] = None
    body_html: Optional[str] = None
    attachment_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CreateSideConversationCmd:
    message: SideConversationMessageCmd
    external_ids: Optional[dict] = None


@dataclass(frozen=True, slots=True)
class ReplySideConversationCmd:
    message: SideConversationMessageCmd


@dataclass(frozen=True, slots=True)
class UpdateSideConversationCmd:
    state: Optional[str] = None
