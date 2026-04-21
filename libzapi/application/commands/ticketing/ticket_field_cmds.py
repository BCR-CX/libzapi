from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, TypeAlias


@dataclass(frozen=True, slots=True)
class CreateTicketFieldCmd:
    title: str
    type: str
    description: str | None = None
    active: bool | None = None
    required: bool | None = None
    collapsed_for_agents: bool | None = None
    regexp_for_validation: str | None = None
    title_in_portal: str | None = None
    visible_in_portal: bool | None = None
    editable_in_portal: bool | None = None
    required_in_portal: bool | None = None
    agent_can_edit: bool | None = None
    tag: str | None = None
    position: int | None = None
    custom_field_options: Iterable[dict[str, Any]] | None = None
    sub_type_id: int | None = None
    relationship_target_type: str | None = None
    relationship_filter: dict[str, Any] | None = None
    agent_description: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateTicketFieldCmd:
    title: str | None = None
    description: str | None = None
    active: bool | None = None
    required: bool | None = None
    collapsed_for_agents: bool | None = None
    regexp_for_validation: str | None = None
    title_in_portal: str | None = None
    visible_in_portal: bool | None = None
    editable_in_portal: bool | None = None
    required_in_portal: bool | None = None
    agent_can_edit: bool | None = None
    tag: str | None = None
    position: int | None = None
    custom_field_options: Iterable[dict[str, Any]] | None = None
    sub_type_id: int | None = None
    relationship_target_type: str | None = None
    relationship_filter: dict[str, Any] | None = None
    agent_description: str | None = None


@dataclass(frozen=True, slots=True)
class TicketFieldOptionCmd:
    name: str
    value: str
    id: int | None = None


TicketFieldCmd: TypeAlias = CreateTicketFieldCmd | UpdateTicketFieldCmd
