import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.bookmark_cmds import CreateBookmarkCmd
from libzapi.application.services.ticketing.bookmarks_service import BookmarksService
from libzapi.domain.errors import Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return BookmarksService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list_all() is sentinel.items
        client.list.assert_called_once_with()

    def test_create_builds_cmd(self):
        service, client = _make_service()
        client.create.return_value = sentinel.bookmark
        result = service.create(42)
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateBookmarkCmd)
        assert cmd.ticket_id == 42
        assert result is sentinel.bookmark

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(bookmark_id=5)


def test_propagates_unauthorized():
    service, client = _make_service()
    client.list.side_effect = Unauthorized("x")
    with pytest.raises(Unauthorized):
        service.list_all()
