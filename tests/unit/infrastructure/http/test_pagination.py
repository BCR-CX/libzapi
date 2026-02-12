from hypothesis import given
from hypothesis.provisional import urls
from hypothesis.strategies import composite, lists, integers, text, dictionaries, booleans, none

from libzapi.infrastructure.http.pagination import _extract_next_page_link


@composite
def build_offset_pagination_data(draw) -> dict:
    return {
        "users": draw(lists(dictionaries(text(), text()))),
        "count": draw(integers()),
        "next_page": draw(urls() | none()),
        "previous_page": draw(urls() | none()),
    }


@composite
def build_cursor_pagination_data(draw) -> dict:
    return {
        "tickets": draw(lists(dictionaries(text(), text()))),
        "meta": {"has_more": draw(booleans()), "after_cursor": draw(text()), "before_cursor": draw(text())},
        "links": {"next": draw(urls() | none()), "prev": draw(urls() | none())},
    }


@given(build_offset_pagination_data() | build_cursor_pagination_data())
def test_extract_next_link(data):
    nxt_link = _extract_next_page_link(data)
    if data.get("next_page") or data.get("links", {}).get("next"):
        assert nxt_link is not None
    else:
        assert nxt_link is None
