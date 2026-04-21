from __future__ import annotations

from typing import Any, Iterable, Iterator

from libzapi.application.commands.ticketing.ticket_field_cmds import (
    CreateTicketFieldCmd,
    TicketFieldOptionCmd,
    UpdateTicketFieldCmd,
)
from libzapi.domain.models.ticketing.ticket_field import TicketField
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.ticket_field_mapper import (
    option_to_payload,
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class TicketFieldApiClient:
    """HTTP adapter for Zendesk Ticket Fields with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[TicketField]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/ticket_fields",
            base_url=self._http.base_url,
            items_key="ticket_fields",
        ):
            yield to_domain(data=obj, cls=TicketField)

    def get(self, field_id: int) -> TicketField:
        data = self._http.get(f"/api/v2/ticket_fields/{int(field_id)}")
        return to_domain(data=data["ticket_field"], cls=TicketField)

    def create(self, entity: CreateTicketFieldCmd) -> TicketField:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/ticket_fields", payload)
        return to_domain(data=data["ticket_field"], cls=TicketField)

    def update(self, field_id: int, entity: UpdateTicketFieldCmd) -> TicketField:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/ticket_fields/{int(field_id)}", payload)
        return to_domain(data=data["ticket_field"], cls=TicketField)

    def delete(self, field_id: int) -> None:
        self._http.delete(f"/api/v2/ticket_fields/{int(field_id)}")

    def reorder(self, field_ids: Iterable[int]) -> None:
        payload = {"ticket_field_ids": [int(i) for i in field_ids]}
        self._http.put("/api/v2/ticket_fields/reorder", payload)

    def list_options(self, field_id: int) -> Iterator[dict[str, Any]]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/ticket_fields/{int(field_id)}/options",
            base_url=self._http.base_url,
            items_key="custom_field_options",
        ):
            yield obj

    def get_option(self, field_id: int, option_id: int) -> dict[str, Any]:
        data = self._http.get(
            f"/api/v2/ticket_fields/{int(field_id)}/options/{int(option_id)}"
        )
        return data["custom_field_option"]

    def upsert_option(
        self, field_id: int, option: TicketFieldOptionCmd
    ) -> dict[str, Any]:
        payload = option_to_payload(option)
        data = self._http.post(
            f"/api/v2/ticket_fields/{int(field_id)}/options", payload
        )
        return data["custom_field_option"]

    def delete_option(self, field_id: int, option_id: int) -> None:
        self._http.delete(
            f"/api/v2/ticket_fields/{int(field_id)}/options/{int(option_id)}"
        )
