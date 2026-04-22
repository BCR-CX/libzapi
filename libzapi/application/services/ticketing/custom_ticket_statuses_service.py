from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.custom_ticket_status_cmds import (
    CreateCustomTicketStatusCmd,
    UpdateCustomTicketStatusCmd,
)
from libzapi.domain.models.ticketing.custom_ticket_status import CustomTicketStatus
from libzapi.infrastructure.api_clients.ticketing.custom_ticket_status_api_client import (
    CustomTicketStatusApiClient,
)


class CustomTicketStatusesService:
    """High-level service for Zendesk Custom Ticket Statuses."""

    def __init__(self, client: CustomTicketStatusApiClient) -> None:
        self._client = client

    def list_all(
        self,
        *,
        status_categories: Iterable[str] | None = None,
        active: bool | None = None,
        default: bool | None = None,
    ) -> Iterable[CustomTicketStatus]:
        return self._client.list(
            status_categories=status_categories, active=active, default=default
        )

    def get_by_id(self, status_id: int) -> CustomTicketStatus:
        return self._client.get(status_id=status_id)

    def create(
        self,
        status_category: str,
        agent_label: str,
        **fields,
    ) -> CustomTicketStatus:
        return self._client.create(
            entity=CreateCustomTicketStatusCmd(
                status_category=status_category,
                agent_label=agent_label,
                **fields,
            )
        )

    def update(self, status_id: int, **fields) -> CustomTicketStatus:
        return self._client.update(
            status_id=status_id,
            entity=UpdateCustomTicketStatusCmd(**fields),
        )
