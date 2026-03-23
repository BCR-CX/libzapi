from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.message_cmds import PostMessageCmd
from libzapi.domain.models.conversations.message import Message
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.mappers.conversations.message_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class MessageApiClient:
    """HTTP adapter for Sunshine Conversations Messages."""

    _BASE = "/v2/apps/{app_id}/conversations/{conversation_id}/messages"

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str, conversation_id: str) -> Iterator[Message]:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=path,
            items_key="messages",
        ):
            yield to_domain(data=obj, cls=Message)

    def post(self, app_id: str, conversation_id: str, cmd: PostMessageCmd) -> Message:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        payload = to_payload_create(cmd)
        data = self._http.post(path, payload)
        return to_domain(data=data["message"], cls=Message)

    def delete_all(self, app_id: str, conversation_id: str) -> None:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        self._http.delete(path)

    def delete(self, app_id: str, conversation_id: str, message_id: str) -> None:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        self._http.delete(f"{path}/{message_id}")
