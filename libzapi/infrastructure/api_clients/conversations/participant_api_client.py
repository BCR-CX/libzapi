from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.conversations.participant import Participant
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain


class ParticipantApiClient:
    """HTTP adapter for Sunshine Conversations Participants."""

    _BASE = "/v2/apps/{app_id}/conversations/{conversation_id}/participants"

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str, conversation_id: str) -> Iterator[Participant]:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        data = self._http.get(path)
        for obj in data.get("participants", []):
            yield to_domain(data=obj, cls=Participant)

    def join(self, app_id: str, conversation_id: str, user_id: str) -> dict:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        return self._http.post(f"{path}/join", {"userId": user_id})

    def leave(self, app_id: str, conversation_id: str, user_id: str) -> None:
        path = self._BASE.format(app_id=app_id, conversation_id=conversation_id)
        self._http.post(f"{path}/leave", {"userId": user_id})
