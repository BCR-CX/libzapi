from __future__ import annotations

from typing import Any, Iterable

from libzapi.application.commands.ticketing.automation_cmds import (
    CreateAutomationCmd,
    UpdateAutomationCmd,
)
from libzapi.domain.models.ticketing.automation import Automation
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing import AutomationApiClient


class AutomationsService:
    """High-level service using the API client."""

    def __init__(self, client: AutomationApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Automation]:
        return self._client.list_all()

    def list_active(self) -> Iterable[Automation]:
        return self._client.list_active()

    def search(self, query: str) -> Iterable[Automation]:
        return self._client.search(query=query)

    def get(self, automation_id: int) -> Automation:
        return self._client.get(automation_id=automation_id)

    def create(self, **fields) -> Automation:
        return self._client.create(entity=CreateAutomationCmd(**fields))

    def update(self, automation_id: int, **fields) -> Automation:
        return self._client.update(
            automation_id=automation_id, entity=UpdateAutomationCmd(**fields)
        )

    def delete(self, automation_id: int) -> None:
        self._client.delete(automation_id=automation_id)

    def create_many(
        self, automations: Iterable[dict[str, Any]]
    ) -> JobStatus:
        return self._client.create_many(
            entities=[CreateAutomationCmd(**a) for a in automations]
        )

    def update_many(
        self, updates: Iterable[tuple[int, dict[str, Any]]]
    ) -> JobStatus:
        pairs = [
            (automation_id, UpdateAutomationCmd(**fields))
            for automation_id, fields in updates
        ]
        return self._client.update_many(updates=pairs)

    def destroy_many(
        self, automation_ids: Iterable[int]
    ) -> JobStatus:
        return self._client.destroy_many(automation_ids=automation_ids)
