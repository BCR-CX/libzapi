from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.automation_cmds import (
    CreateAutomationCmd,
    UpdateAutomationCmd,
)
from libzapi.domain.models.ticketing.automation import Automation
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.automation_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class AutomationApiClient:
    """HTTP adapter for Zendesk Automations"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Automation]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/automations",
            base_url=self._http.base_url,
            items_key="automations",
        ):
            yield to_domain(data=obj, cls=Automation)

    def list_active(self) -> Iterator[Automation]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/automations/active",
            base_url=self._http.base_url,
            items_key="automations",
        ):
            yield to_domain(data=obj, cls=Automation)

    def search(self, query: str) -> Iterator[Automation]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/automations/search?query={query}",
            base_url=self._http.base_url,
            items_key="automations",
        ):
            yield to_domain(data=obj, cls=Automation)

    def get(self, automation_id: int) -> Automation:
        data = self._http.get(f"/api/v2/automations/{int(automation_id)}")
        return to_domain(data=data["automation"], cls=Automation)

    def create(self, entity: CreateAutomationCmd) -> Automation:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/automations", payload)
        return to_domain(data=data["automation"], cls=Automation)

    def update(
        self, automation_id: int, entity: UpdateAutomationCmd
    ) -> Automation:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/automations/{int(automation_id)}", payload
        )
        return to_domain(data=data["automation"], cls=Automation)

    def delete(self, automation_id: int) -> None:
        self._http.delete(f"/api/v2/automations/{int(automation_id)}")

    def create_many(
        self, entities: Iterable[CreateAutomationCmd]
    ) -> JobStatus:
        payload = {
            "automations": [to_payload_create(e)["automation"] for e in entities]
        }
        data = self._http.post("/api/v2/automations/create_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many(
        self, updates: Iterable[tuple[int, UpdateAutomationCmd]]
    ) -> JobStatus:
        items = []
        for automation_id, cmd in updates:
            item = to_payload_update(cmd)["automation"]
            item["id"] = int(automation_id)
            items.append(item)
        data = self._http.put(
            "/api/v2/automations/update_many", {"automations": items}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, automation_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in automation_ids)
        data = (
            self._http.delete(
                f"/api/v2/automations/destroy_many?ids={ids_str}"
            )
            or {}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)
