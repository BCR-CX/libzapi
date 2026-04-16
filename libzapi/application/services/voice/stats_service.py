from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.voice.stats import AccountOverview, AgentActivity, AgentsOverview, CurrentQueueActivity
from libzapi.infrastructure.api_clients.voice.stats_api_client import StatsApiClient


class StatsService:
    def __init__(self, client: StatsApiClient) -> None:
        self._client = client

    def account_overview(self, phone_number_ids: Iterable[int] | None = None) -> AccountOverview:
        return self._client.account_overview(phone_number_ids=phone_number_ids)

    def agents_activity(self, group_ids: Iterable[int] | None = None) -> list[AgentActivity]:
        return self._client.agents_activity(group_ids=group_ids)

    def agents_overview(self) -> AgentsOverview:
        return self._client.agents_overview()

    def current_queue_activity(self, phone_number_ids: Iterable[int] | None = None) -> CurrentQueueActivity:
        return self._client.current_queue_activity(phone_number_ids=phone_number_ids)
