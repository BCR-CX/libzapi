from __future__ import annotations

from libzapi.infrastructure.api_clients.conversations.participant_api_client import ParticipantApiClient


class ParticipantsService:
    """High-level service for Sunshine Conversations Participants."""

    def __init__(self, client: ParticipantApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self, conversation_id: str):
        return self._client.list_all(self._app_id, conversation_id)

    def join(self, conversation_id: str, user_id: str):
        return self._client.join(self._app_id, conversation_id, user_id)

    def leave(self, conversation_id: str, user_id: str) -> None:
        self._client.leave(self._app_id, conversation_id, user_id)
