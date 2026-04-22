from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.domain.models.ticketing.comment import Comment
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class TicketCommentApiClient:
    """HTTP adapter for Zendesk Ticket Comments."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        ticket_id: int,
        *,
        include_inline_images: bool | None = None,
        sort_order: str | None = None,
    ) -> Iterator[Comment]:
        path = f"/api/v2/tickets/{int(ticket_id)}/comments"
        params: list[str] = []
        if include_inline_images is not None:
            params.append(
                "include_inline_images=" + ("true" if include_inline_images else "false")
            )
        if sort_order is not None:
            params.append(f"sort_order={sort_order}")
        if params:
            path = f"{path}?{'&'.join(params)}"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="comments",
        ):
            yield to_domain(data=obj, cls=Comment)

    def count(self, ticket_id: int) -> int:
        data = self._http.get(f"/api/v2/tickets/{int(ticket_id)}/comments/count")
        return int(data["count"]["value"])

    def redact(
        self,
        ticket_id: int,
        comment_id: int,
        text: str,
    ) -> Comment:
        data = self._http.put(
            f"/api/v2/tickets/{int(ticket_id)}/comments/{int(comment_id)}/redact",
            {"text": text},
        )
        return to_domain(data=data["comment"], cls=Comment)

    def make_private(self, ticket_id: int, comment_id: int) -> None:
        self._http.put(
            f"/api/v2/tickets/{int(ticket_id)}/comments/{int(comment_id)}/make_private",
            {},
        )

    def redact_attachment(
        self,
        ticket_id: int,
        comment_id: int,
        attachment_id: int,
    ) -> Comment:
        data = self._http.put(
            f"/api/v2/tickets/{int(ticket_id)}/comments/{int(comment_id)}/attachments/{int(attachment_id)}/redact",
            {},
        )
        return to_domain(data=data["comment"], cls=Comment)

    def redact_chat_comment(
        self,
        ticket_id: int,
        comment_id: int,
        chat_id: str,
        message_ids: Iterable[str],
        external_attachment_urls: Iterable[str] | None = None,
    ) -> Comment:
        payload: dict = {
            "chat_id": chat_id,
            "message_ids": list(message_ids),
        }
        if external_attachment_urls is not None:
            payload["external_attachment_urls"] = list(external_attachment_urls)
        data = self._http.put(
            f"/api/v2/tickets/{int(ticket_id)}/comments/{int(comment_id)}/redact_chat_comment",
            payload,
        )
        return to_domain(data=data["comment"], cls=Comment)
