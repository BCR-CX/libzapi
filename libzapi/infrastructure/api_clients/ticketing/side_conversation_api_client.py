from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.side_conversation_cmds import (
    CreateSideConversationCmd,
    ReplySideConversationCmd,
    UpdateSideConversationCmd,
)
from libzapi.domain.models.ticketing.side_conversation import SideConversation
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.side_conversation_mapper import (
    to_payload_create,
    to_payload_reply,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class SideConversationApiClient:
    """HTTP adapter for Zendesk Side Conversations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, ticket_id: int) -> Iterator[SideConversation]:
        path = f"/api/v2/tickets/{int(ticket_id)}/side_conversations"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="side_conversations",
        ):
            yield to_domain(data=obj, cls=SideConversation)

    def get(self, ticket_id: int, side_conversation_id: str) -> SideConversation:
        data = self._http.get(
            f"/api/v2/tickets/{int(ticket_id)}/side_conversations/{side_conversation_id}"
        )
        return to_domain(data=data["side_conversation"], cls=SideConversation)

    def create(
        self, ticket_id: int, entity: CreateSideConversationCmd
    ) -> SideConversation:
        data = self._http.post(
            f"/api/v2/tickets/{int(ticket_id)}/side_conversations",
            to_payload_create(entity),
        )
        return to_domain(data=data["side_conversation"], cls=SideConversation)

    def reply(
        self,
        ticket_id: int,
        side_conversation_id: str,
        entity: ReplySideConversationCmd,
    ) -> SideConversation:
        data = self._http.post(
            f"/api/v2/tickets/{int(ticket_id)}/side_conversations/{side_conversation_id}/reply",
            to_payload_reply(entity),
        )
        return to_domain(data=data["side_conversation"], cls=SideConversation)

    def update(
        self,
        ticket_id: int,
        side_conversation_id: str,
        entity: UpdateSideConversationCmd,
    ) -> SideConversation:
        data = self._http.put(
            f"/api/v2/tickets/{int(ticket_id)}/side_conversations/{side_conversation_id}",
            to_payload_update(entity),
        )
        return to_domain(data=data["side_conversation"], cls=SideConversation)

    def list_events(
        self, ticket_id: int, side_conversation_id: str
    ) -> Iterator[dict]:
        path = (
            f"/api/v2/tickets/{int(ticket_id)}/side_conversations/"
            f"{side_conversation_id}/events"
        )
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="events",
        ):
            yield obj
