from __future__ import annotations

from libzapi.domain.models.agent_availability.job_status import JobStatus
from libzapi.domain.models.agent_availability.unified_agent_status import UnifiedAgentStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/agent_availabilities/agent_statuses"


def _flatten_status(item: dict) -> dict:
    """Flatten JSON:API status object into a flat dict. Handles both nested and flat formats."""
    if "attributes" in item:
        attrs = item["attributes"]
        flat = {"id": item["id"]}
        flat["name"] = attrs.get("name", "")
        flat["description"] = attrs.get("description")
        flat["group_ids"] = attrs.get("group_ids", [])
        flat["channels"] = attrs.get("channels")
        flat["updated_at"] = attrs.get("updated_at")
        return flat
    return item


class UnifiedAgentStatusApiClient:
    """HTTP adapter for Zendesk Unified Agent Status."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> list[UnifiedAgentStatus]:
        data = self._http.get(_BASE)
        results = []
        for item in data.get("default_statuses", data.get("default", [])):
            results.append(to_domain(data=_flatten_status(item), cls=UnifiedAgentStatus))
        for item in data.get("custom_statuses", data.get("custom", [])):
            results.append(to_domain(data=_flatten_status(item), cls=UnifiedAgentStatus))
        return results

    def list_me(self) -> list[UnifiedAgentStatus]:
        data = self._http.get(f"{_BASE}/me")
        results = []
        for item in data.get("default_statuses", data.get("default", [])):
            results.append(to_domain(data=_flatten_status(item), cls=UnifiedAgentStatus))
        for item in data.get("custom_statuses", data.get("custom", [])):
            results.append(to_domain(data=_flatten_status(item), cls=UnifiedAgentStatus))
        return results

    def update_agent(self, agent_id: int, status_id: int) -> dict:
        payload = {"id": status_id}
        return self._http.put(f"{_BASE}/agents/{int(agent_id)}", payload)

    def update_me(self, status_id: int) -> dict:
        payload = {"id": status_id}
        return self._http.put(f"{_BASE}/agents/me", payload)

    def bulk_update(self, agent_ids: list[int], status_id: int) -> dict:
        ids_param = ",".join(str(i) for i in agent_ids)
        payload = {"id": status_id}
        return self._http.put(f"{_BASE}/agents/update_many?ids={ids_param}", payload)

    def get_job_status(self, job_id: str) -> JobStatus:
        data = self._http.get(f"{_BASE}/job_statuses/{job_id}")
        return to_domain(data=data, cls=JobStatus)
