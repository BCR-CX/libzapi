from __future__ import annotations

from libzapi.application.commands.conversations.conversation_cmds import CreateConversationCmd, UpdateConversationCmd
from libzapi.infrastructure.api_clients.conversations.conversation_api_client import ConversationApiClient


class ConversationsService:
    """High-level service for Sunshine Conversations Conversations."""

    def __init__(self, client: ConversationApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_by_user(self, user_id: str):
        return self._client.list_by_user(self._app_id, user_id)

    def get(self, conversation_id: str):
        return self._client.get(self._app_id, conversation_id)

    def create(self, type: str = "personal", **kwargs):
        cmd = CreateConversationCmd(type=type, **kwargs)
        return self._client.create(self._app_id, cmd)

    def update(self, conversation_id: str, **kwargs):
        cmd = UpdateConversationCmd(**kwargs)
        return self._client.update(self._app_id, conversation_id, cmd)

    def delete(self, conversation_id: str) -> None:
        self._client.delete(self._app_id, conversation_id)
