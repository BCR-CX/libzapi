from __future__ import annotations

from typing import Iterable, Iterator
from urllib.parse import urlencode

from libzapi.application.commands.ticketing.custom_ticket_status_cmds import (
    CreateCustomTicketStatusCmd,
    UpdateCustomTicketStatusCmd,
)
from libzapi.domain.models.ticketing.custom_ticket_status import CustomTicketStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.custom_ticket_status_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class CustomTicketStatusApiClient:
    """HTTP adapter for Zendesk Custom Ticket Statuses."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        status_categories: Iterable[str] | None = None,
        active: bool | None = None,
        default: bool | None = None,
    ) -> Iterator[CustomTicketStatus]:
        query: dict = {}
        if status_categories is not None:
            query["status_categories"] = ",".join(status_categories)
        if active is not None:
            query["active"] = "true" if active else "false"
        if default is not None:
            query["default"] = "true" if default else "false"
        path = "/api/v2/custom_statuses"
        if query:
            path = f"{path}?{urlencode(query)}"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="custom_statuses",
        ):
            yield to_domain(data=obj, cls=CustomTicketStatus)

    def get(self, status_id: int) -> CustomTicketStatus:
        data = self._http.get(f"/api/v2/custom_statuses/{int(status_id)}")
        return to_domain(data=data["custom_status"], cls=CustomTicketStatus)

    def create(self, entity: CreateCustomTicketStatusCmd) -> CustomTicketStatus:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/custom_statuses", payload)
        return to_domain(data=data["custom_status"], cls=CustomTicketStatus)

    def update(
        self, status_id: int, entity: UpdateCustomTicketStatusCmd
    ) -> CustomTicketStatus:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/custom_statuses/{int(status_id)}", payload
        )
        return to_domain(data=data["custom_status"], cls=CustomTicketStatus)
