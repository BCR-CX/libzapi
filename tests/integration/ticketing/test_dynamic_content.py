import itertools

import pytest

from libzapi import Ticketing


def test_list_items(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.dynamic_content.list_items(), 20))
    assert isinstance(items, list)


def test_get_unknown_raises(ticketing: Ticketing):
    from libzapi.domain.errors import NotFound

    with pytest.raises(NotFound):
        ticketing.dynamic_content.get_item(999999999)


def test_list_variants_for_known_item(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.dynamic_content.list_items(), 1))
    if not items:
        pytest.skip("No dynamic content items on this tenant.")
    variants = list(
        itertools.islice(
            ticketing.dynamic_content.list_variants(items[0].id), 20
        )
    )
    assert isinstance(variants, list)
