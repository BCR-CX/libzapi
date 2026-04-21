from __future__ import annotations

from typing import Any, Iterable

from libzapi.application.commands.ticketing.ticket_field_cmds import (
    CreateTicketFieldCmd,
    TicketFieldOptionCmd,
    UpdateTicketFieldCmd,
)
from libzapi.domain.models.ticketing.ticket_field import TicketField
from libzapi.infrastructure.api_clients.ticketing.ticket_field_api_client import (
    TicketFieldApiClient,
)


class TicketFieldsService:
    """High-level service using the API client."""

    def __init__(self, client: TicketFieldApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[TicketField]:
        return self._client.list()

    def get_by_id(self, field_id: int) -> TicketField:
        return self._client.get(field_id=field_id)

    def create(self, **fields) -> TicketField:
        return self._client.create(entity=CreateTicketFieldCmd(**fields))

    def update(self, field_id: int, **fields) -> TicketField:
        return self._client.update(
            field_id=field_id, entity=UpdateTicketFieldCmd(**fields)
        )

    def delete(self, field_id: int) -> None:
        self._client.delete(field_id=field_id)

    def reorder(self, field_ids: Iterable[int]) -> None:
        self._client.reorder(field_ids=field_ids)

    def list_options(self, field_id: int) -> Iterable[dict[str, Any]]:
        return self._client.list_options(field_id=field_id)

    def get_option(self, field_id: int, option_id: int) -> dict[str, Any]:
        return self._client.get_option(field_id=field_id, option_id=option_id)

    def upsert_option(
        self, field_id: int, name: str, value: str, id: int | None = None
    ) -> dict[str, Any]:
        return self._client.upsert_option(
            field_id=field_id,
            option=TicketFieldOptionCmd(name=name, value=value, id=id),
        )

    def delete_option(self, field_id: int, option_id: int) -> None:
        self._client.delete_option(field_id=field_id, option_id=option_id)
