import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.request_cmds import (
    CreateRequestCmd,
    UpdateRequestCmd,
)
from libzapi.application.services.ticketing.requests_service import (
    RequestsService,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)


def _make_service(client=None):
    client = client or Mock()
    return RequestsService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list_all() is sentinel.items

    def test_list_by_user_delegates(self):
        service, client = _make_service()
        client.list_user.return_value = sentinel.items
        assert service.list_by_user(5) is sentinel.items
        client.list_user.assert_called_once_with(5)

    def test_search_delegates(self):
        service, client = _make_service()
        client.search.return_value = sentinel.items
        assert service.search("q") is sentinel.items
        client.search.assert_called_once_with("q")

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.item
        assert service.get_by_id(7) is sentinel.item
        client.get.assert_called_once_with(7)

    def test_list_comments_delegates(self):
        service, client = _make_service()
        client.list_comments.return_value = sentinel.items
        assert service.list_comments(7) is sentinel.items
        client.list_comments.assert_called_once_with(7)

    def test_get_comment_delegates(self):
        service, client = _make_service()
        client.get_comment.return_value = sentinel.item
        assert service.get_comment(7, 9) is sentinel.item
        client.get_comment.assert_called_once_with(request_id=7, comment_id=9)


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.req

        result = service.create(subject="S", comment={"body": "hi"})

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateRequestCmd)
        assert cmd.subject == "S"
        assert cmd.comment == {"body": "hi"}
        assert result is sentinel.req


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.req

        result = service.update(7, solved=True)

        assert client.update.call_args.kwargs["request_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateRequestCmd)
        assert cmd.solved is True
        assert result is sentinel.req

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.comment is None
        assert cmd.solved is None


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(subject="S", comment={"body": "hi"})

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_all_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()
