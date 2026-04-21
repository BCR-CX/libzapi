import pytest

from libzapi.application.commands.ticketing.request_cmds import (
    CreateRequestCmd,
    UpdateRequestCmd,
)
from libzapi.infrastructure.api_clients.ticketing.request_api_client import (
    RequestApiClient,
)


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.request_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.request_api_client.yield_items"
    )


def test_list_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}])
    client = RequestApiClient(http)
    result = list(client.list())
    assert result[0]["_cls"] == "Request"
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/requests"
    assert kwargs["items_key"] == "requests"


def test_list_user_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}])
    client = RequestApiClient(http)
    result = list(client.list_user(user_id=5))
    assert result[0]["_cls"] == "Request"
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/users/5/requests"


def test_search_yields_items_and_encodes_query(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}])
    client = RequestApiClient(http)
    result = list(client.search(query="hello world"))
    assert result[0]["_cls"] == "Request"
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/requests/search?query=hello%20world"


def test_get_reads_request_key(http, domain):
    http.get.return_value = {"request": {"id": 7, "subject": "S"}}
    client = RequestApiClient(http)
    result = client.get(request_id=7)
    http.get.assert_called_with("/api/v2/requests/7")
    assert result["_cls"] == "Request"


def test_create_posts_payload(http, domain):
    http.post.return_value = {"request": {"id": 1, "subject": "S"}}
    client = RequestApiClient(http)
    client.create(CreateRequestCmd(subject="S", comment={"body": "hi"}))
    http.post.assert_called_with(
        "/api/v2/requests",
        {"request": {"subject": "S", "comment": {"body": "hi"}}},
    )


def test_update_puts_payload(http, domain):
    http.put.return_value = {"request": {"id": 1, "status": "solved"}}
    client = RequestApiClient(http)
    client.update(request_id=1, entity=UpdateRequestCmd(solved=True))
    http.put.assert_called_with(
        "/api/v2/requests/1", {"request": {"solved": True}}
    )


def test_list_comments_yields_items(http, yield_items):
    yield_items.return_value = iter([{"id": 1}, {"id": 2}])
    client = RequestApiClient(http)
    result = list(client.list_comments(request_id=7))
    assert [c["id"] for c in result] == [1, 2]
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/requests/7/comments"
    assert kwargs["items_key"] == "comments"


def test_get_comment_reads_comment_key(http):
    http.get.return_value = {"comment": {"id": 9, "body": "hi"}}
    client = RequestApiClient(http)
    result = client.get_comment(request_id=7, comment_id=9)
    http.get.assert_called_with("/api/v2/requests/7/comments/9")
    assert result == {"id": 9, "body": "hi"}
