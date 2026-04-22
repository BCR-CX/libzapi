import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.side_conversation_cmds import (
    CreateSideConversationCmd,
    ReplySideConversationCmd,
    UpdateSideConversationCmd,
)
from libzapi.application.services.ticketing.side_conversations_service import (
    SideConversationsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return SideConversationsService(client), client


class TestDelegation:
    def test_list_for_ticket_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list_for_ticket(42) is sentinel.items
        client.list.assert_called_once_with(ticket_id=42)

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.sc
        assert service.get(42, "abc") is sentinel.sc
        client.get.assert_called_once_with(ticket_id=42, side_conversation_id="abc")

    def test_list_events_delegates(self):
        service, client = _make_service()
        client.list_events.return_value = sentinel.events
        assert service.list_events(42, "abc") is sentinel.events
        client.list_events.assert_called_once_with(
            ticket_id=42, side_conversation_id="abc"
        )


class TestCreate:
    def test_builds_minimal_cmd(self):
        service, client = _make_service()
        client.create.return_value = sentinel.sc
        result = service.create(ticket_id=42, body="hello")
        call = client.create.call_args
        assert call.kwargs["ticket_id"] == 42
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, CreateSideConversationCmd)
        assert cmd.message.body == "hello"
        assert cmd.message.to == []
        assert cmd.external_ids is None
        assert result is sentinel.sc

    def test_builds_full_cmd(self):
        service, client = _make_service()
        service.create(
            ticket_id=42,
            body="b",
            subject="s",
            to=[{"email": "x@example.com"}],
            from_={"support_address_id": 1},
            body_html="<p>b</p>",
            attachment_ids=["a1"],
            external_ids={"k": "v"},
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.message.subject == "s"
        assert cmd.message.to == [{"email": "x@example.com"}]
        assert cmd.message.from_ == {"support_address_id": 1}
        assert cmd.message.body_html == "<p>b</p>"
        assert cmd.message.attachment_ids == ["a1"]
        assert cmd.external_ids == {"k": "v"}


class TestReply:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.reply.return_value = sentinel.sc
        result = service.reply(
            ticket_id=42,
            side_conversation_id="abc",
            body="r",
            body_html="<p>r</p>",
            attachment_ids=["a1"],
        )
        call = client.reply.call_args
        assert call.kwargs["ticket_id"] == 42
        assert call.kwargs["side_conversation_id"] == "abc"
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, ReplySideConversationCmd)
        assert cmd.message.body == "r"
        assert cmd.message.body_html == "<p>r</p>"
        assert cmd.message.attachment_ids == ["a1"]
        assert result is sentinel.sc


class TestUpdate:
    def test_update_delegates(self):
        service, client = _make_service()
        service.update(ticket_id=42, side_conversation_id="abc", state="closed")
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateSideConversationCmd)
        assert cmd.state == "closed"

    def test_close_sets_state_closed(self):
        service, client = _make_service()
        service.close(ticket_id=42, side_conversation_id="abc")
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.state == "closed"


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_for_ticket(42)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_create_propagates_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(ticket_id=1, body="x")
