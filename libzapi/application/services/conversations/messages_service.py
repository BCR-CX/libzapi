from __future__ import annotations

from libzapi.application.commands.conversations.message_cmds import PostMessageCmd
from libzapi.infrastructure.api_clients.conversations.message_api_client import MessageApiClient


class MessagesService:
    """High-level service for Sunshine Conversations Messages."""

    def __init__(self, client: MessageApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self, conversation_id: str):
        return self._client.list_all(self._app_id, conversation_id)

    def post(self, conversation_id: str, author: dict, content: dict, **kwargs):
        cmd = PostMessageCmd(author=author, content=content, **kwargs)
        return self._client.post(self._app_id, conversation_id, cmd)

    def delete_all(self, conversation_id: str) -> None:
        self._client.delete_all(self._app_id, conversation_id)

    def delete(self, conversation_id: str, message_id: str) -> None:
        self._client.delete(self._app_id, conversation_id, message_id)
