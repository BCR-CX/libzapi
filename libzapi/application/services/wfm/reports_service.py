from typing import Iterable

from libzapi.domain.models.wfm.report import ReportRow
from libzapi.infrastructure.api_clients.wfm import ReportApiClient


class ReportsService:
    def __init__(self, client: ReportApiClient) -> None:
        self._client = client

    def get_data(self, template_id: str, start_time: int, end_time: int) -> Iterable[ReportRow]:
        return self._client.get_data(template_id=template_id, start_time=start_time, end_time=end_time)

    def get_data_with_relationships(self, template_id: str, start_time: int, end_time: int) -> dict:
        return self._client.get_data_with_relationships(
            template_id=template_id, start_time=start_time, end_time=end_time
        )
