from dataclasses import dataclass
from typing import List, Iterable, TypeAlias

from libzapi.domain.models.ticketing.ticket import CustomField


@dataclass(frozen=True, slots=True)
class CreateTicketCmd:
    subject: str
    custom_fields: Iterable[CustomField]
    description: str
    priority: str = ""
    type: str = ""
    group_id: int = None
    requester_id: int = None
    organization_id: int = None
    problem_id: int = None
    tags: Iterable[str] = None
    ticket_form_id: int = None
    brand_id: int = None


@dataclass(frozen=True, slots=True)
class UpdateTicketCmd:
    # partial update intent
    subject: str | None = None
    custom_fields: List[CustomField] | None = None
    description: str | None = None
    priority: str | None = None
    type: str | None = None
    group_id: int | None = None
    requester_id: int | None = None
    organization_id: int | None = None
    problem_id: int | None = None
    tags: list[str] | None = None
    ticket_form_id: int | None = None
    brand_id: int | None = None


@dataclass(frozen=True, slots=True)
class MergeTicketsCmd:
    source_ids: Iterable[int]
    target_comment: str | None = None
    source_comment: str | None = None
    target_comment_is_public: bool = False
    source_comment_is_public: bool = False


TicketCmd: TypeAlias = CreateTicketCmd | UpdateTicketCmd
