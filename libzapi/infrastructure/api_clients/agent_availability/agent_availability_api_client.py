from __future__ import annotations
from typing import Iterable

from libzapi.domain.models.agent_availability.agent_availability import AgentAvailability
from libzapi.domain.models.agent_availability.work_item import WorkItem
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_pages
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/agent_availabilities"


def _flatten_jsonapi(item: dict, included_map: dict | None = None) -> dict:
    """Flatten a JSON:API resource object into a flat dict for cattrs."""
    flat = {"id": item["id"], **item.get("attributes", {})}
    if included_map:
        rel_channels = item.get("relationships", {}).get("channels", {}).get("data", [])
        flat["channels"] = [included_map[c["id"]] for c in rel_channels if c["id"] in included_map]
    return flat


def _build_included_map(included: list[dict]) -> dict:
    """Build a lookup of included resources by id, flattening attributes."""
    result = {}
    for inc in included:
        result[inc["id"]] = {"id": inc["id"], **inc.get("attributes", {})}
    return result


class AgentAvailabilityApiClient:
    """HTTP adapter for Zendesk Agent Availability (JSON:API format)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterable[AgentAvailability]:
        for page in yield_pages(self._http.get, _BASE, self._http.base_url):
            inc_map = _build_included_map(page.get("included", []))
            for item in page.get("data", []):
                yield to_domain(data=_flatten_jsonapi(item, inc_map), cls=AgentAvailability)

    def get(self, agent_id: int) -> AgentAvailability:
        data = self._http.get(f"{_BASE}/{int(agent_id)}")
        inc_map = _build_included_map(data.get("included", []))
        return to_domain(data=_flatten_jsonapi(data["data"], inc_map), cls=AgentAvailability)

    def get_me(self) -> AgentAvailability:
        data = self._http.get(f"{_BASE}/me")
        inc_map = _build_included_map(data.get("included", []))
        return to_domain(data=_flatten_jsonapi(data["data"], inc_map), cls=AgentAvailability)

    def work_items(self, agent_id: int, channel: str) -> Iterable[WorkItem]:
        path = f"{_BASE}/{int(agent_id)}/channels/{channel}/relationships/work_items"
        data = self._http.get(path)
        for item in data.get("data", []):
            yield to_domain(data=_flatten_jsonapi(item), cls=WorkItem)

    def my_work_items(self, channel: str) -> Iterable[WorkItem]:
        path = f"{_BASE}/me/channels/{channel}/relationships/work_items"
        data = self._http.get(path)
        for item in data.get("data", []):
            yield to_domain(data=_flatten_jsonapi(item), cls=WorkItem)
