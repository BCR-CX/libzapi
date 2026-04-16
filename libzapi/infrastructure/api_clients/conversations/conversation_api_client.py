from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.conversation_cmds import CreateConversationCmd, UpdateConversationCmd
from libzapi.domain.models.conversations.conversation import Conversation
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.mappers.conversations.conversation_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class ConversationApiClient:
    """HTTP adapter for Sunshine Conversations Conversations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_by_user(self, app_id: str, user_id: str) -> Iterator[Conversation]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/conversations?filter[userId]={user_id}",
            items_key="conversations",
        ):
            yield to_domain(data=obj, cls=Conversation)

    def get(self, app_id: str, conversation_id: str) -> Conversation:
        data = self._http.get(f"/v2/apps/{app_id}/conversations/{conversation_id}")
        return to_domain(data=data["conversation"], cls=Conversation)

    def create(self, app_id: str, cmd: CreateConversationCmd) -> Conversation:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/v2/apps/{app_id}/conversations", payload)
        return to_domain(data=data["conversation"], cls=Conversation)

    def update(self, app_id: str, conversation_id: str, cmd: UpdateConversationCmd) -> Conversation:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"/v2/apps/{app_id}/conversations/{conversation_id}", payload)
        return to_domain(data=data["conversation"], cls=Conversation)

    def delete(self, app_id: str, conversation_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/conversations/{conversation_id}")
