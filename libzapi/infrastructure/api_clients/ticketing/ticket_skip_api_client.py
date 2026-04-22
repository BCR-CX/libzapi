from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.ticket_skip_cmds import CreateTicketSkipCmd
from libzapi.domain.models.ticketing.ticket_skip import TicketSkip
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.ticket_skip_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class TicketSkipApiClient:
    """HTTP adapter for Zendesk Ticket Skips."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[TicketSkip]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/skips",
            base_url=self._http.base_url,
            items_key="skips",
        ):
            yield to_domain(data=obj, cls=TicketSkip)

    def list_by_user(self, user_id: int) -> Iterator[TicketSkip]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/users/{int(user_id)}/skips",
            base_url=self._http.base_url,
            items_key="skips",
        ):
            yield to_domain(data=obj, cls=TicketSkip)

    def list_by_ticket(self, ticket_id: int) -> Iterator[TicketSkip]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/tickets/{int(ticket_id)}/skips",
            base_url=self._http.base_url,
            items_key="skips",
        ):
            yield to_domain(data=obj, cls=TicketSkip)

    def create(self, ticket_id: int, entity: CreateTicketSkipCmd) -> TicketSkip:
        payload = to_payload_create(entity)
        data = self._http.post(
            f"/api/v2/tickets/{int(ticket_id)}/skips", payload
        )
        return to_domain(data=data["skip"], cls=TicketSkip)
