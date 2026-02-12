from __future__ import annotations
from typing import Iterator


def _extract_next_page_link(data: dict) -> str | None:
    """
    Extract the next pagination link based on the default Zendesk pagination styles.
    Check first for cursor pagination style, then try offset pagination style,
    Zendesk returns a string with a link to the next page or null.

    Some API Routes have a pagination limit, search API with only 11 pages, or 1000
    results.

    REFERENCE: https://developer.zendesk.com/api-reference/introduction/pagination
    """
    nxt = None
    links = data.get("links") or {}
    if not (nxt := links.get("next")):
        nxt = data.get("next_page")
    return nxt


def next_link(data: dict, base_url: str) -> str | None:
    """
    Zendesk style cursor link extractor.
    Accepts absolute or relative next links and returns a relative path.
    """
    if not (nxt := _extract_next_page_link(data)):
        return None
    return nxt.replace(base_url, "") if isinstance(nxt, str) and nxt.startswith("https://") else nxt


def yield_pages(get_json, first_path: str, base_url: str) -> Iterator[dict]:
    """
    Generic pager. get_json is a callable like http.get that returns a dict.
    Yields the full page payload dict so callers can choose the list key.
    """
    path = first_path
    while path:
        data = get_json(path)
        yield data
        path = next_link(data, base_url)


def yield_items(get_json, first_path: str, base_url: str, items_key: str) -> Iterator[dict]:
    """
    Convenience iterator that yields individual items from a list key.
    """
    for page in yield_pages(get_json, first_path, base_url):
        for obj in page.get(items_key, []) or []:
            yield obj
