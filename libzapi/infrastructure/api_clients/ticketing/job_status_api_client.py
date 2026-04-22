from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class JobStatusApiClient:
    """HTTP adapter for Zendesk Job Statuses."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[JobStatus]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/job_statuses",
            base_url=self._http.base_url,
            items_key="job_statuses",
        ):
            yield to_domain(data=obj, cls=JobStatus)

    def get(self, job_id: str) -> JobStatus:
        data = self._http.get(f"/api/v2/job_statuses/{job_id}")
        return to_domain(data=data["job_status"], cls=JobStatus)

    def show_many(self, job_ids: Iterable[str]) -> list[JobStatus]:
        ids_str = ",".join(str(i) for i in job_ids)
        data = self._http.get(f"/api/v2/job_statuses/show_many?ids={ids_str}")
        return [
            to_domain(data=obj, cls=JobStatus)
            for obj in data.get("job_statuses", []) or []
        ]
