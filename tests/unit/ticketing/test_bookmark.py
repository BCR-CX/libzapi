import pytest

from libzapi.application.commands.ticketing.bookmark_cmds import CreateBookmarkCmd
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized
from libzapi.infrastructure.api_clients.ticketing import BookmarkApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.bookmark_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "bookmarks": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = BookmarkApiClient(http)
    items = list(client.list())
    assert len(items) == 2
    assert all(i["_cls"] == "Bookmark" for i in items)
    http.get.assert_called_with("/api/v2/bookmarks")


def test_create_posts_payload(http, domain):
    http.post.return_value = {"bookmark": {"id": 1}}
    client = BookmarkApiClient(http)
    result = client.create(CreateBookmarkCmd(ticket_id=42))
    assert result["_cls"] == "Bookmark"
    http.post.assert_called_with("/api/v2/bookmarks", {"bookmark": {"ticket_id": 42}})


def test_delete(http):
    client = BookmarkApiClient(http)
    client.delete(5)
    http.delete.assert_called_with("/api/v2/bookmarks/5")


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, RateLimited])
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = BookmarkApiClient(http)
    with pytest.raises(error_cls):
        list(client.list())


def test_bookmark_logical_key():
    from libzapi.domain.models.ticketing.bookmark import Bookmark

    bookmark = Bookmark(id=7)
    assert bookmark.logical_key.as_str() == "bookmark:bookmark_id_7"
