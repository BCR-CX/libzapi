from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.ticketing.attachment import Attachment
from libzapi.domain.models.ticketing.suspended_ticket import SuspendedTicket
from libzapi.infrastructure.api_clients.ticketing import (
    SuspendedTicketApiClient,
)


class SuspendedTicketsService:
    """High-level service using the API client."""

    def __init__(self, client: SuspendedTicketApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[SuspendedTicket]:
        return self._client.list()

    def get_by_id(self, id_: int) -> SuspendedTicket:
        return self._client.get(id_)

    def recover(self, id_: int) -> SuspendedTicket:
        return self._client.recover(id_)

    def recover_many(self, ids: Iterable[int]) -> dict:
        return self._client.recover_many(ids)

    def delete(self, id_: int) -> None:
        self._client.delete(id_)

    def destroy_many(self, ids: Iterable[int]) -> dict:
        return self._client.destroy_many(ids)

    def list_attachments(self, id_: int) -> list[Attachment]:
        return self._client.list_attachments(id_)
