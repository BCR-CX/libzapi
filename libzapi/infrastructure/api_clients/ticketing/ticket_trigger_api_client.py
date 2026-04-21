from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.ticket_trigger_cmds import (
    CreateTicketTriggerCmd,
    UpdateTicketTriggerCmd,
)
from libzapi.domain.models.ticketing.ticket_trigger import TicketTrigger
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.ticket_trigger_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class TicketTriggerApiClient:
    """HTTP adapter for Zendesk Ticket Trigger with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[TicketTrigger]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/triggers",
            base_url=self._http.base_url,
            items_key="triggers",
        ):
            yield to_domain(data=obj, cls=TicketTrigger)

    def list_active(self) -> Iterator[TicketTrigger]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/triggers/active",
            base_url=self._http.base_url,
            items_key="triggers",
        ):
            yield to_domain(data=obj, cls=TicketTrigger)

    def search(self, query: str) -> Iterator[TicketTrigger]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/triggers/search?query={query}",
            base_url=self._http.base_url,
            items_key="triggers",
        ):
            yield to_domain(data=obj, cls=TicketTrigger)

    def list_definitions(self) -> dict:
        return self._http.get("/api/v2/triggers/definitions")

    def get(self, trigger_id: int) -> TicketTrigger:
        data = self._http.get(f"/api/v2/triggers/{int(trigger_id)}")
        return to_domain(data=data["trigger"], cls=TicketTrigger)

    def create(self, entity: CreateTicketTriggerCmd) -> TicketTrigger:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/triggers", payload)
        return to_domain(data=data["trigger"], cls=TicketTrigger)

    def update(
        self, trigger_id: int, entity: UpdateTicketTriggerCmd
    ) -> TicketTrigger:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/triggers/{int(trigger_id)}", payload)
        return to_domain(data=data["trigger"], cls=TicketTrigger)

    def delete(self, trigger_id: int) -> None:
        self._http.delete(f"/api/v2/triggers/{int(trigger_id)}")

    def create_many(
        self, entities: Iterable[CreateTicketTriggerCmd]
    ) -> JobStatus:
        payload = {
            "triggers": [to_payload_create(e)["trigger"] for e in entities]
        }
        data = self._http.post("/api/v2/triggers/create_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many(
        self, updates: Iterable[tuple[int, UpdateTicketTriggerCmd]]
    ) -> JobStatus:
        items = []
        for trigger_id, cmd in updates:
            item = to_payload_update(cmd)["trigger"]
            item["id"] = int(trigger_id)
            items.append(item)
        data = self._http.put(
            "/api/v2/triggers/update_many", {"triggers": items}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, trigger_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in trigger_ids)
        data = (
            self._http.delete(f"/api/v2/triggers/destroy_many?ids={ids_str}")
            or {}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)
