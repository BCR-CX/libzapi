from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.wfm.shift_cmds import FetchShiftsCmd
from libzapi.domain.models.wfm.shift import Shift
from libzapi.infrastructure.api_clients.wfm import ShiftApiClient


class ShiftsService:
    def __init__(self, client: ShiftApiClient) -> None:
        self._client = client

    def fetch(
        self,
        start_date: str,
        end_date: str,
        agent_ids: list[int] | None = None,
        published: int | None = None,
        page: int = 1,
    ) -> Iterable[Shift]:
        cmd = FetchShiftsCmd(
            startDate=start_date,
            endDate=end_date,
            agentIds=agent_ids,
            published=published,
            page=page,
        )
        return self._client.fetch(cmd=cmd)
