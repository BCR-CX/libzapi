from __future__ import annotations

from libzapi.infrastructure.http.client import HttpClient

_BASE = "/api/v2/channels/voice/calls"


class RecordingApiClient:
    """HTTP adapter for Zendesk Voice Call Recordings"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def delete_all(self, call_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(call_id)}/recordings")

    def delete_by_type(self, call_id: int, recording_type: str) -> None:
        self._http.delete(f"{_BASE}/{int(call_id)}/recordings/{recording_type}")
