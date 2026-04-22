import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.search_service import SearchService
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return SearchService(client), client


class TestDelegation:
    def test_search_delegates(self):
        service, client = _make_service()
        client.search.return_value = sentinel.items
        assert service.search("q") is sentinel.items
        client.search.assert_called_once_with(
            query="q", sort_by=None, sort_order=None
        )

    def test_search_forwards_sort_params(self):
        service, client = _make_service()
        service.search("q", sort_by="created_at", sort_order="desc")
        client.search.assert_called_once_with(
            query="q", sort_by="created_at", sort_order="desc"
        )

    def test_count_delegates(self):
        service, client = _make_service()
        client.count.return_value = 42
        assert service.count("q") == 42
        client.count.assert_called_once_with(query="q")

    def test_export_delegates(self):
        service, client = _make_service()
        client.export.return_value = sentinel.items
        assert service.export("q", filter_type="ticket") is sentinel.items
        client.export.assert_called_once_with(
            query="q", filter_type="ticket", page_size=None
        )

    def test_export_forwards_page_size(self):
        service, client = _make_service()
        service.export("q", filter_type="user", page_size=500)
        client.export.assert_called_once_with(
            query="q", filter_type="user", page_size=500
        )


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_search_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.search.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.search("q")
