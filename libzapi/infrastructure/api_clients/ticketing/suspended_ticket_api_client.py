from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.domain.models.ticketing.attachment import Attachment
from libzapi.domain.models.ticketing.suspended_ticket import SuspendedTicket
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class SuspendedTicketApiClient:
    """HTTP adapter for Zendesk Suspended Tickets."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[SuspendedTicket]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/suspended_tickets",
            base_url=self._http.base_url,
            items_key="suspended_tickets",
        ):
            yield to_domain(data=obj, cls=SuspendedTicket)

    def get(self, id_: int) -> SuspendedTicket:
        data = self._http.get(f"/api/v2/suspended_tickets/{int(id_)}")
        return to_domain(data=data["suspended_ticket"], cls=SuspendedTicket)

    def recover(self, id_: int) -> SuspendedTicket:
        data = self._http.put(
            f"/api/v2/suspended_tickets/{int(id_)}/recover", {}
        )
        return to_domain(data=data["suspended_ticket"], cls=SuspendedTicket)

    def recover_many(self, ids: Iterable[int]) -> dict:
        ids_str = ",".join(str(int(i)) for i in ids)
        return (
            self._http.put(
                f"/api/v2/suspended_tickets/recover_many?ids={ids_str}", {}
            )
            or {}
        )

    def delete(self, id_: int) -> None:
        self._http.delete(f"/api/v2/suspended_tickets/{int(id_)}")

    def destroy_many(self, ids: Iterable[int]) -> dict:
        ids_str = ",".join(str(int(i)) for i in ids)
        return (
            self._http.delete(
                f"/api/v2/suspended_tickets/destroy_many?ids={ids_str}"
            )
            or {}
        )

    def list_attachments(self, id_: int) -> list[Attachment]:
        data = self._http.get(
            f"/api/v2/suspended_tickets/{int(id_)}/attachments"
        )
        return [
            to_domain(data=item, cls=Attachment)
            for item in (data.get("attachments") or [])
        ]
