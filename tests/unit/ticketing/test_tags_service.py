import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.tags_service import TagsService
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return TagsService(client), client


class TestDelegation:
    def test_list_account_delegates(self):
        service, client = _make_service()
        client.list_account.return_value = sentinel.iter
        assert service.list_account() is sentinel.iter
        client.list_account.assert_called_once_with()

    def test_list_for_delegates(self):
        service, client = _make_service()
        client.list_for.return_value = ["a", "b"]
        result = service.list_for("ticket", 42)
        client.list_for.assert_called_once_with(
            resource="ticket", resource_id=42
        )
        assert result == ["a", "b"]

    def test_add_delegates(self):
        service, client = _make_service()
        client.add.return_value = ["a", "b", "c"]
        result = service.add("user", 7, ["c"])
        client.add.assert_called_once_with(
            resource="user", resource_id=7, tags=["c"]
        )
        assert result == ["a", "b", "c"]

    def test_set_delegates(self):
        service, client = _make_service()
        client.set.return_value = ["x"]
        result = service.set("organization", 9, ["x"])
        client.set.assert_called_once_with(
            resource="organization", resource_id=9, tags=["x"]
        )
        assert result == ["x"]

    def test_remove_delegates(self):
        service, client = _make_service()
        client.remove.return_value = []
        result = service.remove("ticket", 1, ["gone"])
        client.remove.assert_called_once_with(
            resource="ticket", resource_id=1, tags=["gone"]
        )
        assert result == []


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_for_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list_for.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_for("ticket", 1)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_add_propagates_error(self, error_cls):
        service, client = _make_service()
        client.add.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.add("ticket", 1, ["x"])
