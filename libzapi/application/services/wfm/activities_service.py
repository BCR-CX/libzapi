from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.wfm.activity import Activity, ActivityTypeRef, AgentRef
from libzapi.infrastructure.api_clients.wfm import ActivityApiClient


class ActivitiesService:
    def __init__(self, client: ActivityApiClient) -> None:
        self._client = client

    def list(self, start_time: int) -> Iterable[Activity]:
        return self._client.list(start_time=start_time)

    def list_with_relationships(self, start_time: int) -> tuple[list[Activity], list[AgentRef], list[ActivityTypeRef]]:
        return self._client.list_with_relationships(start_time=start_time)
