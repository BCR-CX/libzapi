from __future__ import annotations

from typing import Iterator


def sunco_yield_items(http_client, first_path: str, items_key: str, page_size: int = 100) -> Iterator[dict]:
    """Paginator for Sunshine Conversations API.

    Uses ``get_raw`` to send URLs with literal brackets (``page[size]``)
    that the ``requests`` library would otherwise percent-encode.
    Subsequent pages use ``links.next`` from the API response.
    """
    sep = "&" if "?" in first_path else "?"
    url = f"{http_client.base_url}{first_path}{sep}page[size]={page_size}"
    data = http_client.get_raw(url)
    for obj in data.get(items_key, []) or []:
        yield obj

    while True:
        links = data.get("links") or {}
        nxt = links.get("next") if isinstance(links, dict) else None
        if not nxt:
            break
        data = http_client.get_raw(nxt)
        for obj in data.get(items_key, []) or []:
            yield obj
