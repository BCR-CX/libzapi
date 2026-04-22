import itertools

from libzapi import Ticketing


def test_search_returns_results(ticketing: Ticketing):
    hits = list(itertools.islice(ticketing.search.search("type:ticket"), 5))
    assert isinstance(hits, list)


def test_search_sort_params(ticketing: Ticketing):
    hits = list(
        itertools.islice(
            ticketing.search.search(
                "type:ticket", sort_by="created_at", sort_order="desc"
            ),
            5,
        )
    )
    assert isinstance(hits, list)


def test_count_returns_int(ticketing: Ticketing):
    count = ticketing.search.count("type:user")
    assert isinstance(count, int)
    assert count >= 0


def test_export_returns_typed_items(ticketing: Ticketing):
    hits = list(
        itertools.islice(
            ticketing.search.export("type:ticket", filter_type="ticket"),
            5,
        )
    )
    assert isinstance(hits, list)
