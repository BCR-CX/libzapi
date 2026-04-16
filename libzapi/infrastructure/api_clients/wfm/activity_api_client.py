from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.wfm.activity import Activity, ActivityTypeRef, AgentRef
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/wfm/public/api/v1/activities"


class ActivityApiClient:
    """HTTP adapter for WFM Activities API.

    Pagination: pass the last activity's startTime to fetch the next page.
    Max 1000 records per request.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, start_time: int) -> Iterable[Activity]:
        path = f"{_BASE}?startTime={int(start_time)}"
        while path:
            data = self._http.get(path)
            for item in data.get("data", []):
                yield to_domain(data=item, cls=Activity)
            metadata = data.get("metadata") or {}
            next_url = metadata.get("next")
            if next_url and isinstance(next_url, str):
                path = next_url.replace(self._http.base_url, "") if next_url.startswith("https://") else next_url
            else:
                path = None

    def list_with_relationships(self, start_time: int) -> tuple[list[Activity], list[AgentRef], list[ActivityTypeRef]]:
        data = self._http.get(f"{_BASE}?startTime={int(start_time)}")
        activities = [to_domain(data=item, cls=Activity) for item in data.get("data", [])]
        rels = data.get("relationships") or {}
        agents = [to_domain(data=a, cls=AgentRef) for a in rels.get("agent", [])]
        activity_types = [to_domain(data=at, cls=ActivityTypeRef) for at in rels.get("activityType", [])]
        return activities, agents, activity_types
