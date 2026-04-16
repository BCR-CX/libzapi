from __future__ import annotations

from libzapi.application.commands.voice.callback_request_cmds import CreateCallbackRequestCmd
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.callback_request_mapper import to_payload_create

_BASE = "/api/v2/channels/voice/callback_requests"


class CallbackRequestApiClient:
    """HTTP adapter for Zendesk Voice Callback Requests"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, cmd: CreateCallbackRequestCmd) -> dict:
        payload = to_payload_create(cmd)
        return self._http.post(_BASE, json=payload)
