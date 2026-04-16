from __future__ import annotations

from libzapi.application.commands.conversations.switchboard_action_cmds import OfferControlCmd, PassControlCmd
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.conversations.switchboard_action_mapper import (
    to_payload_offer_control,
    to_payload_pass_control,
)


class SwitchboardActionApiClient:
    """HTTP adapter for Sunshine Conversations Switchboard Actions."""

    _BASE = "/v2/apps/{app_id}/conversations/{conversation_id}"

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def accept_control(self, app_id: str, conversation_id: str, metadata: dict | None = None) -> dict:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        payload: dict = {}
        if metadata is not None:
            payload["metadata"] = metadata
        return self._http.post(f"{path}/acceptControl", payload)

    def offer_control(self, app_id: str, conversation_id: str, cmd: OfferControlCmd) -> dict:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        payload = to_payload_offer_control(cmd)
        return self._http.post(f"{path}/offerControl", payload)

    def pass_control(self, app_id: str, conversation_id: str, cmd: PassControlCmd) -> dict:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        payload = to_payload_pass_control(cmd)
        return self._http.post(f"{path}/passControl", payload)

    def release_control(self, app_id: str, conversation_id: str, metadata: dict | None = None) -> dict:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        payload: dict = {}
        if metadata is not None:
            payload["metadata"] = metadata
        return self._http.post(f"{path}/releaseControl", payload)
