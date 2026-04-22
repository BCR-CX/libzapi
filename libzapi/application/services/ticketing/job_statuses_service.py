from __future__ import annotations

import time
from typing import Callable, Iterable, Iterator

from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing.job_status_api_client import (
    JobStatusApiClient,
)


_TERMINAL_STATUSES = frozenset({"completed", "failed", "killed"})


class JobStatusTimeout(Exception):
    """Raised when a job status does not reach a terminal state in time."""


class JobStatusesService:
    """High-level service for Zendesk job statuses."""

    def __init__(self, client: JobStatusApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[JobStatus]:
        return self._client.list()

    def get_by_id(self, job_id: str) -> JobStatus:
        return self._client.get(job_id=job_id)

    def show_many(self, job_ids: Iterable[str]) -> list[JobStatus]:
        return self._client.show_many(job_ids=job_ids)

    def wait_until_complete(
        self,
        job_id: str,
        interval: float = 1.0,
        timeout: float = 60.0,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], float] = time.monotonic,
    ) -> JobStatus:
        """Poll a job status until it reaches a terminal state.

        Raises JobStatusTimeout if the job does not finish within `timeout`
        seconds. `sleep` and `now` are injectable for testing.
        """
        deadline = now() + timeout
        while True:
            status = self._client.get(job_id=job_id)
            if status.status in _TERMINAL_STATUSES:
                return status
            if now() >= deadline:
                raise JobStatusTimeout(
                    f"job {job_id} did not complete within {timeout}s"
                )
            sleep(interval)
