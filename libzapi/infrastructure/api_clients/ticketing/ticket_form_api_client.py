from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.ticket_form_cmds import (
    CreateTicketFormCmd,
    UpdateTicketFormCmd,
)
from libzapi.domain.models.ticketing.ticket_form import TicketForm
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.ticket_form_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class TicketFormApiClient:
    """HTTP adapter for Zendesk Ticket Forms with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[TicketForm]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/ticket_forms",
            base_url=self._http.base_url,
            items_key="ticket_forms",
        ):
            yield to_domain(data=obj, cls=TicketForm)

    def get(self, ticket_form_id: int) -> TicketForm:
        data = self._http.get(f"/api/v2/ticket_forms/{int(ticket_form_id)}")
        return to_domain(data=data["ticket_form"], cls=TicketForm)

    def create(self, entity: CreateTicketFormCmd) -> TicketForm:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/ticket_forms", payload)
        return to_domain(data=data["ticket_form"], cls=TicketForm)

    def update(self, ticket_form_id: int, entity: UpdateTicketFormCmd) -> TicketForm:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/ticket_forms/{int(ticket_form_id)}", payload
        )
        return to_domain(data=data["ticket_form"], cls=TicketForm)

    def delete(self, ticket_form_id: int) -> None:
        self._http.delete(f"/api/v2/ticket_forms/{int(ticket_form_id)}")

    def clone(self, ticket_form_id: int) -> TicketForm:
        data = self._http.post(
            f"/api/v2/ticket_forms/{int(ticket_form_id)}/clone", {}
        )
        return to_domain(data=data["ticket_form"], cls=TicketForm)

    def reorder(self, ticket_form_ids: Iterable[int]) -> None:
        payload = {"ticket_form_ids": [int(i) for i in ticket_form_ids]}
        self._http.put("/api/v2/ticket_forms/reorder", payload)
