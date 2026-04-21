from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.sla_policy_cmds import (
    CreateSlaPolicyCmd,
    UpdateSlaPolicyCmd,
)
from libzapi.domain.models.ticketing.sla_policies import SlaPolicy
from libzapi.infrastructure.api_clients.ticketing.sla_policy_api_client import SlaPolicyApiClient


class SlaPoliciesService:
    """High-level service using the API client."""

    def __init__(self, client: SlaPolicyApiClient) -> None:
        self._client = client

    def list(self) -> Iterable[SlaPolicy]:
        return self._client.list()

    def list_definitions(self) -> dict:
        return self._client.list_definitions()

    def get(self, sla_policy_id: int) -> SlaPolicy:
        return self._client.get(sla_policy_id=sla_policy_id)

    def create(self, **fields) -> SlaPolicy:
        return self._client.create(entity=CreateSlaPolicyCmd(**fields))

    def update(self, sla_policy_id: int, **fields) -> SlaPolicy:
        return self._client.update(
            sla_policy_id=sla_policy_id, entity=UpdateSlaPolicyCmd(**fields)
        )

    def delete(self, sla_policy_id: int) -> None:
        self._client.delete(sla_policy_id=sla_policy_id)

    def reorder(self, sla_policy_ids: Iterable[int]) -> list[SlaPolicy]:
        return self._client.reorder(sla_policy_ids=sla_policy_ids)
