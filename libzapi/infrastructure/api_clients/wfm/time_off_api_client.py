from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.wfm.time_off_cmds import ImportTimeOffCmd
from libzapi.domain.models.wfm.time_off import TimeOff, TimeOffImportResult
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.wfm.time_off_mapper import to_payload_import
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/wfm/public/api/v1/timeOff"


class TimeOffApiClient:
    """HTTP adapter for WFM Time Off API."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

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
        params: list[str] = []
        if time_off_request_id is not None:
            params.append(f"timeOffRequestId={time_off_request_id}")
        if agent_id is not None:
            params.append(f"agentId={int(agent_id)}")
        if start_time is not None:
            params.append(f"startTime={int(start_time)}")
        if end_time is not None:
            params.append(f"endTime={int(end_time)}")
        if status is not None:
            params.append(f"status={status}")
        if reason_id is not None:
            params.append(f"reasonId={reason_id}")
        if time_off_type is not None:
            params.append(f"timeOffType={time_off_type}")
        if page is not None:
            params.append(f"page={int(page)}")
        if per_page is not None:
            params.append(f"perPage={int(per_page)}")

        query = "&".join(params)
        path = f"{_BASE}?{query}" if query else _BASE
        data = self._http.get(path)
        for item in data.get("data", []):
            yield to_domain(data=item, cls=TimeOff)

    def import_time_off(self, cmd: ImportTimeOffCmd) -> TimeOffImportResult:
        payload = to_payload_import(cmd)
        data = self._http.post(f"{_BASE}/import", json=payload)
        return to_domain(data=data.get("data", {}), cls=TimeOffImportResult)
