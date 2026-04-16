from __future__ import annotations

from libzapi.application.commands.voice.callback_request_cmds import CreateCallbackRequestCmd
from libzapi.infrastructure.api_clients.voice.callback_request_api_client import CallbackRequestApiClient


class CallbackRequestsService:
    def __init__(self, client: CallbackRequestApiClient) -> None:
        self._client = client

    def create(self, phone_number_id: int, requester_phone_number: str, group_ids: list[int] | None = None) -> dict:
        cmd = CreateCallbackRequestCmd(
            phone_number_id=phone_number_id,
            requester_phone_number=requester_phone_number,
            group_ids=group_ids or [],
        )
        return self._client.create(cmd=cmd)
