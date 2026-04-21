from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.sla_policy_cmds import (
    CreateSlaPolicyCmd,
    UpdateSlaPolicyCmd,
)
from libzapi.domain.models.ticketing.sla_policies import SlaPolicy
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.sla_policy_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class SlaPolicyApiClient:
    """HTTP adapter for Zendesk Sla Policies with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[SlaPolicy]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/slas/policies",
            base_url=self._http.base_url,
            items_key="sla_policies",
        ):
            yield to_domain(data=obj, cls=SlaPolicy)

    def list_definitions(self) -> dict:
        return self._http.get("/api/v2/slas/policies/definitions")

    def get(self, sla_policy_id: int) -> SlaPolicy:
        data = self._http.get(f"/api/v2/slas/policies/{int(sla_policy_id)}")
        return to_domain(data=data["sla_policy"], cls=SlaPolicy)

    def create(self, entity: CreateSlaPolicyCmd) -> SlaPolicy:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/slas/policies", payload)
        return to_domain(data=data["sla_policy"], cls=SlaPolicy)

    def update(
        self, sla_policy_id: int, entity: UpdateSlaPolicyCmd
    ) -> SlaPolicy:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/slas/policies/{int(sla_policy_id)}", payload
        )
        return to_domain(data=data["sla_policy"], cls=SlaPolicy)

    def delete(self, sla_policy_id: int) -> None:
        self._http.delete(f"/api/v2/slas/policies/{int(sla_policy_id)}")

    def reorder(self, sla_policy_ids: Iterable[int]) -> list[SlaPolicy]:
        ids = [int(i) for i in sla_policy_ids]
        data = self._http.put(
            "/api/v2/slas/policies/reorder", {"sla_policy_ids": ids}
        )
        return [
            to_domain(data=obj, cls=SlaPolicy)
            for obj in data.get("sla_policies", [])
        ]
