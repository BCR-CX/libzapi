from __future__ import annotations

from typing import Iterator
from urllib.parse import urlencode

from libzapi.domain.models.ticketing.ticket_activity import TicketActivity
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class TicketActivityApiClient:
    """HTTP adapter for Zendesk Ticket Activities."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self, *, since: str | None = None, include: str | None = None
    ) -> Iterator[TicketActivity]:
        query: dict = {}
        if since is not None:
            query["since"] = since
        if include is not None:
            query["include"] = include
        path = "/api/v2/activities"
        if query:
            path = f"{path}?{urlencode(query)}"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="activities",
        ):
            yield to_domain(data=obj, cls=TicketActivity)

    def get(self, activity_id: int) -> TicketActivity:
        data = self._http.get(f"/api/v2/activities/{int(activity_id)}")
        return to_domain(data=data["activity"], cls=TicketActivity)
