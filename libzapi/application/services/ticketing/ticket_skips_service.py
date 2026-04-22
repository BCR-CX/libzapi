from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.ticket_skip_cmds import CreateTicketSkipCmd
from libzapi.domain.models.ticketing.ticket_skip import TicketSkip
from libzapi.infrastructure.api_clients.ticketing.ticket_skip_api_client import (
    TicketSkipApiClient,
)


class TicketSkipsService:
    """High-level service for Zendesk Ticket Skips."""

    def __init__(self, client: TicketSkipApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[TicketSkip]:
        return self._client.list()

    def list_by_user(self, user_id: int) -> Iterable[TicketSkip]:
        return self._client.list_by_user(user_id=user_id)

    def list_by_ticket(self, ticket_id: int) -> Iterable[TicketSkip]:
        return self._client.list_by_ticket(ticket_id=ticket_id)

    def create(self, ticket_id: int, reason: str) -> TicketSkip:
        return self._client.create(
            ticket_id=ticket_id, entity=CreateTicketSkipCmd(reason=reason)
        )
