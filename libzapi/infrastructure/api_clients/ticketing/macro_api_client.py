from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.macro_cmds import (
    CreateMacroCmd,
    UpdateMacroCmd,
)
from libzapi.domain.models.ticketing.macro import Macro
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.macro_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class MacroApiClient:
    """HTTP adapter for Zendesk Macros with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Macro]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/macros",
            base_url=self._http.base_url,
            items_key="macros",
        ):
            yield to_domain(data=obj, cls=Macro)

    def list_active(self) -> Iterator[Macro]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/macros/active",
            base_url=self._http.base_url,
            items_key="macros",
        ):
            yield to_domain(data=obj, cls=Macro)

    def search(self, query: str) -> Iterator[Macro]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/macros/search?query={query}",
            base_url=self._http.base_url,
            items_key="macros",
        ):
            yield to_domain(data=obj, cls=Macro)

    def list_categories(self) -> list[str]:
        data = self._http.get("/api/v2/macros/categories")
        return list(data.get("categories", []))

    def list_definitions(self) -> dict:
        return self._http.get("/api/v2/macros/definitions")

    def get(self, macro_id: int) -> Macro:
        data = self._http.get(f"/api/v2/macros/{int(macro_id)}")
        return to_domain(data["macro"], Macro)

    def apply(self, macro_id: int) -> dict:
        data = self._http.get(f"/api/v2/macros/{int(macro_id)}/apply")
        return data.get("result", {})

    def apply_to_ticket(self, ticket_id: int, macro_id: int) -> dict:
        data = self._http.get(
            f"/api/v2/tickets/{int(ticket_id)}/macros/{int(macro_id)}/apply"
        )
        return data.get("result", {})

    def create(self, entity: CreateMacroCmd) -> Macro:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/macros", payload)
        return to_domain(data["macro"], Macro)

    def update(self, macro_id: int, entity: UpdateMacroCmd) -> Macro:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/macros/{int(macro_id)}", payload)
        return to_domain(data["macro"], Macro)

    def delete(self, macro_id: int) -> None:
        self._http.delete(f"/api/v2/macros/{int(macro_id)}")

    def create_many(self, entities: Iterable[CreateMacroCmd]) -> JobStatus:
        payload = {"macros": [to_payload_create(e)["macro"] for e in entities]}
        data = self._http.post("/api/v2/macros/create_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many(
        self, updates: Iterable[tuple[int, UpdateMacroCmd]]
    ) -> JobStatus:
        items = []
        for macro_id, cmd in updates:
            item = to_payload_update(cmd)["macro"]
            item["id"] = int(macro_id)
            items.append(item)
        data = self._http.put("/api/v2/macros/update_many", {"macros": items})
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, macro_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in macro_ids)
        data = (
            self._http.delete(f"/api/v2/macros/destroy_many?ids={ids_str}") or {}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)
