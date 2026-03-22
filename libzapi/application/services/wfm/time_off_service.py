from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.wfm.time_off_cmds import ImportTimeOffCmd, ImportTimeOffEntry
from libzapi.domain.models.wfm.time_off import TimeOff, TimeOffImportResult
from libzapi.infrastructure.api_clients.wfm import TimeOffApiClient


class TimeOffService:
    def __init__(self, client: TimeOffApiClient) -> None:
        self._client = client

    def list(
        self,
        time_off_request_id: str | None = None,
        agent_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        status: str | None = None,
        reason_id: str | None = None,
        time_off_type: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Iterable[TimeOff]:
        return self._client.list(
            time_off_request_id=time_off_request_id,
            agent_id=agent_id,
            start_time=start_time,
            end_time=end_time,
            status=status,
            reason_id=reason_id,
            time_off_type=time_off_type,
            page=page,
            per_page=per_page,
        )

    def import_time_off(self, entries: list[ImportTimeOffEntry]) -> TimeOffImportResult:
        cmd = ImportTimeOffCmd(data=entries)
        return self._client.import_time_off(cmd=cmd)
