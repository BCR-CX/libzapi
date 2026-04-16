from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.voice.stats import (
    AccountOverview,
    AgentActivity,
    AgentsOverview,
    CurrentQueueActivity,
)
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/stats"


class StatsApiClient:
    """HTTP adapter for Zendesk Voice Stats"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def account_overview(self, phone_number_ids: Iterable[int] | None = None) -> AccountOverview:
        path = f"{_BASE}/account_overview"
        if phone_number_ids is not None:
            ids_str = ",".join(str(i) for i in phone_number_ids)
            path = f"{path}?phone_number_ids={ids_str}"
        data = self._http.get(path)
        return to_domain(data=data["account_overview"], cls=AccountOverview)

    def agents_activity(self, group_ids: Iterable[int] | None = None) -> list[AgentActivity]:
        path = f"{_BASE}/agents_activity"
        if group_ids is not None:
            ids_str = ",".join(str(i) for i in group_ids)
            path = f"{path}?group_ids={ids_str}"
        data = self._http.get(path)
        return [to_domain(data=obj, cls=AgentActivity) for obj in data["agents_activity"]]

    def agents_overview(self) -> AgentsOverview:
        data = self._http.get(f"{_BASE}/agents_overview")
        return to_domain(data=data["agents_overview"], cls=AgentsOverview)

    def current_queue_activity(self, phone_number_ids: Iterable[int] | None = None) -> CurrentQueueActivity:
        path = f"{_BASE}/current_queue_activity"
        if phone_number_ids is not None:
            ids_str = ",".join(str(i) for i in phone_number_ids)
            path = f"{path}?phone_number_ids={ids_str}"
        data = self._http.get(path)
        return to_domain(data=data["current_queue_activity"], cls=CurrentQueueActivity)
