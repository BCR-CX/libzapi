import itertools

import pytest

from libzapi import Ticketing


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.organization_fields.list_all(), 20))
    assert isinstance(items, list)


def test_get_unknown_raises(ticketing: Ticketing):
    from libzapi.domain.errors import NotFound

    with pytest.raises(NotFound):
        ticketing.organization_fields.get_by_id(999999999)
