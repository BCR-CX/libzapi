import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.ticket_comments_service import (
    TicketCommentsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return TicketCommentsService(client), client


class TestDelegation:
    def test_list_for_ticket_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.iter
        assert service.list_for_ticket(42) is sentinel.iter
        client.list.assert_called_once_with(
            ticket_id=42, include_inline_images=None, sort_order=None
        )

    def test_list_for_ticket_passes_kwargs(self):
        service, client = _make_service()
        client.list.return_value = sentinel.iter
        service.list_for_ticket(
            42, include_inline_images=True, sort_order="desc"
        )
        client.list.assert_called_once_with(
            ticket_id=42, include_inline_images=True, sort_order="desc"
        )

    def test_count_delegates(self):
        service, client = _make_service()
        client.count.return_value = 5
        assert service.count(42) == 5
        client.count.assert_called_once_with(ticket_id=42)

    def test_redact_delegates(self):
        service, client = _make_service()
        client.redact.return_value = sentinel.comment
        assert service.redact(42, 9, "secret") is sentinel.comment
        client.redact.assert_called_once_with(
            ticket_id=42, comment_id=9, text="secret"
        )

    def test_make_private_delegates(self):
        service, client = _make_service()
        service.make_private(42, 9)
        client.make_private.assert_called_once_with(ticket_id=42, comment_id=9)

    def test_redact_attachment_delegates(self):
        service, client = _make_service()
        client.redact_attachment.return_value = sentinel.comment
        assert (
            service.redact_attachment(42, 9, 3) is sentinel.comment
        )
        client.redact_attachment.assert_called_once_with(
            ticket_id=42, comment_id=9, attachment_id=3
        )

    def test_redact_chat_comment_delegates(self):
        service, client = _make_service()
        client.redact_chat_comment.return_value = sentinel.comment
        service.redact_chat_comment(
            ticket_id=42,
            comment_id=9,
            chat_id="c",
            message_ids=["m1"],
        )
        client.redact_chat_comment.assert_called_once_with(
            ticket_id=42,
            comment_id=9,
            chat_id="c",
            message_ids=["m1"],
            external_attachment_urls=None,
        )

    def test_redact_chat_comment_passes_external_urls(self):
        service, client = _make_service()
        service.redact_chat_comment(
            ticket_id=42,
            comment_id=9,
            chat_id="c",
            message_ids=["m1"],
            external_attachment_urls=["https://x/y.png"],
        )
        assert (
            client.redact_chat_comment.call_args.kwargs[
                "external_attachment_urls"
            ]
            == ["https://x/y.png"]
        )


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_count_propagates_error(self, error_cls):
        service, client = _make_service()
        client.count.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.count(1)
