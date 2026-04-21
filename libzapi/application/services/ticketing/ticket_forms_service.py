from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.ticket_form_cmds import (
    CreateTicketFormCmd,
    UpdateTicketFormCmd,
)
from libzapi.domain.models.ticketing.ticket_form import TicketForm
from libzapi.infrastructure.api_clients.ticketing.ticket_form_api_client import (
    TicketFormApiClient,
)


class TicketFormsService:
    """High-level service using the API client."""

    def __init__(self, client: TicketFormApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[TicketForm]:
        return self._client.list()

    def get_by_id(self, ticket_form_id: int) -> TicketForm:
        return self._client.get(ticket_form_id=ticket_form_id)

    def create(self, **fields) -> TicketForm:
        return self._client.create(entity=CreateTicketFormCmd(**fields))

    def update(self, ticket_form_id: int, **fields) -> TicketForm:
        return self._client.update(
            ticket_form_id=ticket_form_id, entity=UpdateTicketFormCmd(**fields)
        )

    def delete(self, ticket_form_id: int) -> None:
        self._client.delete(ticket_form_id=ticket_form_id)

    def clone(self, ticket_form_id: int) -> TicketForm:
        return self._client.clone(ticket_form_id=ticket_form_id)

    def reorder(self, ticket_form_ids: Iterable[int]) -> None:
        self._client.reorder(ticket_form_ids=ticket_form_ids)
