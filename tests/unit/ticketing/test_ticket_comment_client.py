import pytest

from libzapi.domain.errors import NotFound, Unauthorized
from libzapi.infrastructure.api_clients.ticketing import TicketCommentApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_comment_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_comment_api_client.yield_items"
    )


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_list_hits_expected_path(http, yield_items, domain):
    yield_items.return_value = iter([{"id": 1}])
    client = TicketCommentApiClient(http)
    list(client.list(42))
    yield_items.assert_called_once_with(
        get_json=http.get,
        first_path="/api/v2/tickets/42/comments",
        base_url=http.base_url,
        items_key="comments",
    )


def test_list_with_include_inline_images_true(http, yield_items, domain):
    yield_items.return_value = iter([])
    client = TicketCommentApiClient(http)
    list(client.list(42, include_inline_images=True))
    assert (
        yield_items.call_args.kwargs["first_path"]
        == "/api/v2/tickets/42/comments?include_inline_images=true"
    )


def test_list_with_include_inline_images_false(http, yield_items, domain):
    yield_items.return_value = iter([])
    client = TicketCommentApiClient(http)
    list(client.list(42, include_inline_images=False))
    assert (
        yield_items.call_args.kwargs["first_path"]
        == "/api/v2/tickets/42/comments?include_inline_images=false"
    )


def test_list_with_sort_order(http, yield_items, domain):
    yield_items.return_value = iter([])
    client = TicketCommentApiClient(http)
    list(client.list(42, sort_order="desc"))
    assert (
        yield_items.call_args.kwargs["first_path"]
        == "/api/v2/tickets/42/comments?sort_order=desc"
    )


def test_list_combines_params(http, yield_items, domain):
    yield_items.return_value = iter([])
    client = TicketCommentApiClient(http)
    list(client.list(42, include_inline_images=True, sort_order="desc"))
    assert (
        yield_items.call_args.kwargs["first_path"]
        == "/api/v2/tickets/42/comments?include_inline_images=true&sort_order=desc"
    )


def test_list_yields_parsed_items(http, yield_items, domain):
    yield_items.return_value = iter([{"id": 1}, {"id": 2}])
    client = TicketCommentApiClient(http)
    items = list(client.list(42))
    assert len(items) == 2
    assert items[0]["_cls"] == "Comment"


# ---------------------------------------------------------------------------
# count
# ---------------------------------------------------------------------------


def test_count_returns_value(http):
    http.get.return_value = {"count": {"value": 17, "refreshed_at": "now"}}
    client = TicketCommentApiClient(http)
    assert client.count(42) == 17
    http.get.assert_called_with("/api/v2/tickets/42/comments/count")


# ---------------------------------------------------------------------------
# redact
# ---------------------------------------------------------------------------


def test_redact_puts_payload(http, domain):
    http.put.return_value = {"comment": {"id": 9}}
    client = TicketCommentApiClient(http)
    result = client.redact(ticket_id=42, comment_id=9, text="secret")
    http.put.assert_called_with(
        "/api/v2/tickets/42/comments/9/redact",
        {"text": "secret"},
    )
    assert result["_cls"] == "Comment"


# ---------------------------------------------------------------------------
# make_private
# ---------------------------------------------------------------------------


def test_make_private_puts_empty_body(http):
    client = TicketCommentApiClient(http)
    client.make_private(ticket_id=42, comment_id=9)
    http.put.assert_called_with(
        "/api/v2/tickets/42/comments/9/make_private", {}
    )


# ---------------------------------------------------------------------------
# redact_attachment
# ---------------------------------------------------------------------------


def test_redact_attachment_puts_empty_body(http, domain):
    http.put.return_value = {"comment": {"id": 9}}
    client = TicketCommentApiClient(http)
    result = client.redact_attachment(
        ticket_id=42, comment_id=9, attachment_id=3
    )
    http.put.assert_called_with(
        "/api/v2/tickets/42/comments/9/attachments/3/redact", {}
    )
    assert result["_cls"] == "Comment"


# ---------------------------------------------------------------------------
# redact_chat_comment
# ---------------------------------------------------------------------------


def test_redact_chat_comment_puts_payload(http, domain):
    http.put.return_value = {"comment": {"id": 9}}
    client = TicketCommentApiClient(http)
    client.redact_chat_comment(
        ticket_id=42,
        comment_id=9,
        chat_id="chat-1",
        message_ids=iter(["m1", "m2"]),
    )
    http.put.assert_called_with(
        "/api/v2/tickets/42/comments/9/redact_chat_comment",
        {"chat_id": "chat-1", "message_ids": ["m1", "m2"]},
    )


def test_redact_chat_comment_includes_external_urls(http, domain):
    http.put.return_value = {"comment": {"id": 9}}
    client = TicketCommentApiClient(http)
    client.redact_chat_comment(
        ticket_id=42,
        comment_id=9,
        chat_id="chat-1",
        message_ids=["m1"],
        external_attachment_urls=["https://x/y.png"],
    )
    http.put.assert_called_with(
        "/api/v2/tickets/42/comments/9/redact_chat_comment",
        {
            "chat_id": "chat-1",
            "message_ids": ["m1"],
            "external_attachment_urls": ["https://x/y.png"],
        },
    )


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_count_propagates_error(error_cls, http):
    http.get.side_effect = error_cls("boom")
    client = TicketCommentApiClient(http)
    with pytest.raises(error_cls):
        client.count(1)
