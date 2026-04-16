from __future__ import annotations

from libzapi.infrastructure.api_clients.voice.recording_api_client import RecordingApiClient


class RecordingsService:
    def __init__(self, client: RecordingApiClient) -> None:
        self._client = client

    def delete_all(self, call_id: int) -> None:
        self._client.delete_all(call_id=call_id)

    def delete_by_type(self, call_id: int, recording_type: str) -> None:
        self._client.delete_by_type(call_id=call_id, recording_type=recording_type)
