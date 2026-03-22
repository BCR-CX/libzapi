from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.wfm.shift_cmds import FetchShiftsCmd
from libzapi.domain.models.wfm.shift import Shift
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.wfm.shift_mapper import to_payload_fetch
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/wfm/public/api/v1/shifts/fetch"


class ShiftApiClient:
    """HTTP adapter for WFM Shifts API."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def fetch(self, cmd: FetchShiftsCmd) -> Iterable[Shift]:
        payload = to_payload_fetch(cmd)
        data = self._http.post(_BASE, json=payload)
        for item in data.get("data", []):
            yield to_domain(data=item, cls=Shift)
