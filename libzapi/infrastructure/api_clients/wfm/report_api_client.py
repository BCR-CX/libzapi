from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.wfm.report import ReportRow
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/wfm/public/api/v1/reports"


class ReportApiClient:
    """HTTP adapter for WFM Reports API."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_data(self, template_id: str, start_time: int, end_time: int) -> Iterable[ReportRow]:
        path = f"{_BASE}/{template_id}/data?startTime={int(start_time)}&endTime={int(end_time)}"
        data = self._http.get(path)
        for item in data.get("data", []):
            yield to_domain(data=item, cls=ReportRow)

    def get_data_with_relationships(self, template_id: str, start_time: int, end_time: int) -> dict:
        path = f"{_BASE}/{template_id}/data?startTime={int(start_time)}&endTime={int(end_time)}"
        return self._http.get(path)
