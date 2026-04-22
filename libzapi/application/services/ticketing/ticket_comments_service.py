from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.domain.models.ticketing.comment import Comment
from libzapi.infrastructure.api_clients.ticketing.ticket_comment_api_client import (
    TicketCommentApiClient,
)


class TicketCommentsService:
    """High-level service for Zendesk ticket comments."""

    def __init__(self, client: TicketCommentApiClient) -> None:
        self._client = client

    def list_for_ticket(
        self,
        ticket_id: int,
        *,
        include_inline_images: bool | None = None,
        sort_order: str | None = None,
    ) -> Iterator[Comment]:
        return self._client.list(
            ticket_id=ticket_id,
            include_inline_images=include_inline_images,
            sort_order=sort_order,
        )

    def count(self, ticket_id: int) -> int:
        return self._client.count(ticket_id=ticket_id)

    def redact(self, ticket_id: int, comment_id: int, text: str) -> Comment:
        return self._client.redact(
            ticket_id=ticket_id, comment_id=comment_id, text=text
        )

    def make_private(self, ticket_id: int, comment_id: int) -> None:
        self._client.make_private(ticket_id=ticket_id, comment_id=comment_id)

    def redact_attachment(
        self, ticket_id: int, comment_id: int, attachment_id: int
    ) -> Comment:
        return self._client.redact_attachment(
            ticket_id=ticket_id,
            comment_id=comment_id,
            attachment_id=attachment_id,
        )

    def redact_chat_comment(
        self,
        ticket_id: int,
        comment_id: int,
        chat_id: str,
        message_ids: Iterable[str],
        external_attachment_urls: Iterable[str] | None = None,
    ) -> Comment:
        return self._client.redact_chat_comment(
            ticket_id=ticket_id,
            comment_id=comment_id,
            chat_id=chat_id,
            message_ids=message_ids,
            external_attachment_urls=external_attachment_urls,
        )
