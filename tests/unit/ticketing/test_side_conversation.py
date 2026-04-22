import pytest

from libzapi.application.commands.ticketing.side_conversation_cmds import (
    CreateSideConversationCmd,
    ReplySideConversationCmd,
    SideConversationMessageCmd,
    UpdateSideConversationCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import SideConversationApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.side_conversation_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


def test_list_hits_expected_path(http, domain):
    http.get.return_value = {"side_conversations": [{"id": "abc"}]}
    client = SideConversationApiClient(http)
    items = list(client.list(42))
    assert len(items) == 1
    assert items[0]["_cls"] == "SideConversation"
    http.get.assert_called_with("/api/v2/tickets/42/side_conversations")


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "side_conversations": [{"id": "a"}, {"id": "b"}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = SideConversationApiClient(http)
    items = list(client.list(7))
    assert len(items) == 2
    assert all(i["_cls"] == "SideConversation" for i in items)


def test_list_coerces_ticket_id(http, domain):
    http.get.return_value = {"side_conversations": []}
    client = SideConversationApiClient(http)
    list(client.list(ticket_id="5"))  # type: ignore[arg-type]
    http.get.assert_called_with("/api/v2/tickets/5/side_conversations")


def test_get_returns_domain(http, domain):
    http.get.return_value = {"side_conversation": {"id": "abc"}}
    client = SideConversationApiClient(http)
    result = client.get(42, "abc")
    assert result["_cls"] == "SideConversation"
    http.get.assert_called_with("/api/v2/tickets/42/side_conversations/abc")


def test_create_posts_payload(http, domain):
    http.post.return_value = {"side_conversation": {"id": "new"}}
    client = SideConversationApiClient(http)
    cmd = CreateSideConversationCmd(
        message=SideConversationMessageCmd(body="hi", subject="Q")
    )
    client.create(ticket_id=42, entity=cmd)
    http.post.assert_called_with(
        "/api/v2/tickets/42/side_conversations",
        {"side_conversation": {"message": {"body": "hi", "subject": "Q"}}},
    )


def test_reply_posts_payload(http, domain):
    http.post.return_value = {"side_conversation": {"id": "abc"}}
    client = SideConversationApiClient(http)
    cmd = ReplySideConversationCmd(message=SideConversationMessageCmd(body="r"))
    client.reply(ticket_id=42, side_conversation_id="abc", entity=cmd)
    http.post.assert_called_with(
        "/api/v2/tickets/42/side_conversations/abc/reply",
        {"message": {"body": "r"}},
    )


def test_update_puts_payload(http, domain):
    http.put.return_value = {"side_conversation": {"id": "abc"}}
    client = SideConversationApiClient(http)
    cmd = UpdateSideConversationCmd(state="closed")
    client.update(ticket_id=42, side_conversation_id="abc", entity=cmd)
    http.put.assert_called_with(
        "/api/v2/tickets/42/side_conversations/abc",
        {"side_conversation": {"state": "closed"}},
    )


def test_list_events_yields_dicts(http, domain):
    http.get.return_value = {
        "events": [{"id": "e1"}, {"id": "e2"}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = SideConversationApiClient(http)
    events = list(client.list_events(42, "abc"))
    assert events == [{"id": "e1"}, {"id": "e2"}]
    http.get.assert_called_with("/api/v2/tickets/42/side_conversations/abc/events")


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = SideConversationApiClient(http)
    with pytest.raises(error_cls):
        list(client.list(42))


def test_side_conversation_logical_key():
    from libzapi.domain.models.ticketing.side_conversation import SideConversation

    sc = SideConversation(id="abc-123", ticket_id=42)
    assert sc.logical_key.as_str() == "side_conversation:side_conversation_id_abc-123"
