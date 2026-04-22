from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.ticketing.organization import Organization
from libzapi.domain.models.ticketing.ticket import Ticket
from libzapi.domain.models.ticketing.user import User
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/incremental"


class IncrementalExportApiClient:
    """HTTP adapter for Zendesk Ticketing Incremental Export endpoints.

    Time-based endpoints follow ``next_page`` links, cursor-based endpoints
    follow ``after_url`` + ``end_of_stream`` semantics.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    # -----------------------------------------------------------------
    # Time-based exports
    # -----------------------------------------------------------------

    def tickets(self, start_time: int) -> Iterator[Ticket]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/tickets?start_time={int(start_time)}",
            base_url=self._http.base_url,
            items_key="tickets",
        ):
            yield to_domain(data=obj, cls=Ticket)

    def ticket_events(self, start_time: int) -> Iterator[dict]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/ticket_events?start_time={int(start_time)}",
            base_url=self._http.base_url,
            items_key="ticket_events",
        ):
            yield obj

    def users(self, start_time: int) -> Iterator[User]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/users?start_time={int(start_time)}",
            base_url=self._http.base_url,
            items_key="users",
        ):
            yield to_domain(data=obj, cls=User)

    def organizations(self, start_time: int) -> Iterator[Organization]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/organizations?start_time={int(start_time)}",
            base_url=self._http.base_url,
            items_key="organizations",
        ):
            yield to_domain(data=obj, cls=Organization)

    # -----------------------------------------------------------------
    # Cursor-based exports
    # -----------------------------------------------------------------

    def tickets_cursor(self, start_time: int) -> Iterator[Ticket]:
        yield from self._iter_cursor(
            first_path=f"{_BASE}/tickets/cursor?start_time={int(start_time)}",
            items_key="tickets",
            cls=Ticket,
        )

    def users_cursor(self, start_time: int) -> Iterator[User]:
        yield from self._iter_cursor(
            first_path=f"{_BASE}/users/cursor?start_time={int(start_time)}",
            items_key="users",
            cls=User,
        )

    def _iter_cursor(self, first_path: str, items_key: str, cls):
        path: str | None = first_path
        while path:
            page = self._http.get(path)
            for obj in page.get(items_key, []) or []:
                yield to_domain(data=obj, cls=cls)
            if page.get("end_of_stream"):
                return
            after_url = page.get("after_url")
            if not after_url:
                return
            path = (
                after_url.replace(self._http.base_url, "")
                if isinstance(after_url, str) and after_url.startswith("https://")
                else after_url
            )

    # -----------------------------------------------------------------
    # Sample endpoint (one page, no pagination)
    # -----------------------------------------------------------------

    def sample(self, resource: str, start_time: int) -> dict:
        allowed = {"tickets", "users", "organizations", "ticket_events"}
        if resource not in allowed:
            raise ValueError(f"Unknown incremental sample resource: {resource}")
        return self._http.get(
            f"{_BASE}/{resource}/sample?start_time={int(start_time)}"
        )
