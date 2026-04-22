from __future__ import annotations

from typing import Iterator, List, Optional

from libzapi.application.commands.ticketing.side_conversation_cmds import (
    CreateSideConversationCmd,
    ReplySideConversationCmd,
    SideConversationMessageCmd,
    UpdateSideConversationCmd,
)
from libzapi.domain.models.ticketing.side_conversation import SideConversation
from libzapi.infrastructure.api_clients.ticketing.side_conversation_api_client import (
    SideConversationApiClient,
)


class SideConversationsService:
    def __init__(self, client: SideConversationApiClient) -> None:
        self._client = client

    def list_for_ticket(self, ticket_id: int) -> Iterator[SideConversation]:
        return self._client.list(ticket_id=ticket_id)

    def get(self, ticket_id: int, side_conversation_id: str) -> SideConversation:
        return self._client.get(
            ticket_id=ticket_id, side_conversation_id=side_conversation_id
        )

    def create(
        self,
        ticket_id: int,
        *,
        body: str,
        subject: Optional[str] = None,
        to: Optional[List[dict]] = None,
        from_: Optional[dict] = None,
        body_html: Optional[str] = None,
        attachment_ids: Optional[List[str]] = None,
        external_ids: Optional[dict] = None,
    ) -> SideConversation:
        message = SideConversationMessageCmd(
            body=body,
            subject=subject,
            to=list(to) if to else [],
            from_=from_,
            body_html=body_html,
            attachment_ids=list(attachment_ids) if attachment_ids else [],
        )
        cmd = CreateSideConversationCmd(message=message, external_ids=external_ids)
        return self._client.create(ticket_id=ticket_id, entity=cmd)

    def reply(
        self,
        ticket_id: int,
        side_conversation_id: str,
        *,
        body: str,
        body_html: Optional[str] = None,
        attachment_ids: Optional[List[str]] = None,
    ) -> SideConversation:
        message = SideConversationMessageCmd(
            body=body,
            body_html=body_html,
            attachment_ids=list(attachment_ids) if attachment_ids else [],
        )
        cmd = ReplySideConversationCmd(message=message)
        return self._client.reply(
            ticket_id=ticket_id,
            side_conversation_id=side_conversation_id,
            entity=cmd,
        )

    def update(
        self,
        ticket_id: int,
        side_conversation_id: str,
        *,
        state: Optional[str] = None,
    ) -> SideConversation:
        cmd = UpdateSideConversationCmd(state=state)
        return self._client.update(
            ticket_id=ticket_id,
            side_conversation_id=side_conversation_id,
            entity=cmd,
        )

    def close(self, ticket_id: int, side_conversation_id: str) -> SideConversation:
        return self.update(
            ticket_id=ticket_id,
            side_conversation_id=side_conversation_id,
            state="closed",
        )

    def list_events(
        self, ticket_id: int, side_conversation_id: str
    ) -> Iterator[dict]:
        return self._client.list_events(
            ticket_id=ticket_id, side_conversation_id=side_conversation_id
        )
