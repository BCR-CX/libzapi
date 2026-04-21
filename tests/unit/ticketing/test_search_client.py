import pytest

from libzapi.infrastructure.api_clients.ticketing.search_api_client import (
    SearchApiClient,
)


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.search_api_client.yield_items"
    )


def test_search_yields_results(http, yield_items):
    yield_items.return_value = iter([{"id": 1}, {"id": 2}])
    client = SearchApiClient(http)
    result = list(client.search(query="status:open"))
    assert [r["id"] for r in result] == [1, 2]
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/search?query=status%3Aopen"
    assert kwargs["items_key"] == "results"


def test_search_includes_sort_params(http, yield_items):
    yield_items.return_value = iter([])
    client = SearchApiClient(http)
    list(client.search(query="q", sort_by="created_at", sort_order="desc"))
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == (
        "/api/v2/search?query=q&sort_by=created_at&sort_order=desc"
    )


def test_search_omits_none_sort_params(http, yield_items):
    yield_items.return_value = iter([])
    client = SearchApiClient(http)
    list(client.search(query="q"))
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/search?query=q"


def test_count_returns_int(http):
    http.get.return_value = {"count": 42}
    client = SearchApiClient(http)
    assert client.count(query="status:open") == 42
    http.get.assert_called_with("/api/v2/search/count?query=status%3Aopen")


def test_count_defaults_to_zero(http):
    http.get.return_value = {}
    client = SearchApiClient(http)
    assert client.count(query="q") == 0


def test_export_yields_results_with_filter_type(http, yield_items):
    yield_items.return_value = iter([{"id": 1}])
    client = SearchApiClient(http)
    result = list(client.export(query="q", filter_type="ticket"))
    assert result[0]["id"] == 1
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == (
        "/api/v2/search/export?query=q&filter%5Btype%5D=ticket"
    )


def test_export_includes_page_size(http, yield_items):
    yield_items.return_value = iter([])
    client = SearchApiClient(http)
    list(client.export(query="q", filter_type="user", page_size=100))
    kwargs = yield_items.call_args.kwargs
    assert "page%5Bsize%5D=100" in kwargs["first_path"]
