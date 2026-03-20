from __future__ import annotations
from typing import Iterable

from libzapi.domain.models.agent_availability.engagement import Engagement
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/engagements"


class EngagementApiClient:
    """HTTP adapter for Zendesk Omnichannel Engagements (read-only)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        agent_id: int | None = None,
        channel: str | None = None,
        ticket_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        filter_by: str | None = None,
        page_size: int | None = None,
    ) -> Iterable[Engagement]:
        params: list[str] = []
        if agent_id is not None:
            params.append(f"agent_id={agent_id}")
        if channel is not None:
            params.append(f"channel={channel}")
        if ticket_id is not None:
            params.append(f"ticket_id={ticket_id}")
        if start_time is not None:
            params.append(f"start_time={start_time}")
        if end_time is not None:
            params.append(f"end_time={end_time}")
        if filter_by is not None:
            params.append(f"filter_by={filter_by}")
        if page_size is not None:
            params.append(f"page_size={page_size}")
        query = f"?{'&'.join(params)}" if params else ""
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}{query}",
            base_url=self._http.base_url,
            items_key="data",
        ):
            yield to_domain(data=obj, cls=Engagement)

    def get(self, engagement_id: str) -> Engagement:
        data = self._http.get(f"{_BASE}/{engagement_id}")
        return to_domain(data=data["data"], cls=Engagement)
