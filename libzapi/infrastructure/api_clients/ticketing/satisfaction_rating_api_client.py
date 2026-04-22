from __future__ import annotations

from typing import Iterator
from urllib.parse import urlencode

from libzapi.application.commands.ticketing.satisfaction_rating_cmds import (
    CreateSatisfactionRatingCmd,
)
from libzapi.domain.models.ticketing.satisfaction_rating import (
    SatisfactionRating,
    SatisfactionReason,
)
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.satisfaction_rating_mapper import (
    to_payload_create,
)
from libzapi.infrastructure.serialization.parse import to_domain


class SatisfactionRatingApiClient:
    """HTTP adapter for Zendesk Satisfaction Ratings + Reasons."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        score: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> Iterator[SatisfactionRating]:
        query: dict = {}
        if score is not None:
            query["score"] = score
        if start_time is not None:
            query["start_time"] = int(start_time)
        if end_time is not None:
            query["end_time"] = int(end_time)
        path = "/api/v2/satisfaction_ratings"
        if query:
            path = f"{path}?{urlencode(query)}"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="satisfaction_ratings",
        ):
            yield to_domain(data=obj, cls=SatisfactionRating)

    def list_received(self) -> Iterator[SatisfactionRating]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/satisfaction_ratings/received",
            base_url=self._http.base_url,
            items_key="satisfaction_ratings",
        ):
            yield to_domain(data=obj, cls=SatisfactionRating)

    def get(self, rating_id: int) -> SatisfactionRating:
        data = self._http.get(f"/api/v2/satisfaction_ratings/{int(rating_id)}")
        return to_domain(data=data["satisfaction_rating"], cls=SatisfactionRating)

    def create_for_ticket(
        self, ticket_id: int, entity: CreateSatisfactionRatingCmd
    ) -> SatisfactionRating:
        payload = to_payload_create(entity)
        data = self._http.post(
            f"/api/v2/tickets/{int(ticket_id)}/satisfaction_rating", payload
        )
        return to_domain(data=data["satisfaction_rating"], cls=SatisfactionRating)

    def list_reasons(self) -> Iterator[SatisfactionReason]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/satisfaction_reasons",
            base_url=self._http.base_url,
            items_key="reasons",
        ):
            yield to_domain(data=obj, cls=SatisfactionReason)

    def get_reason(self, reason_id: int) -> SatisfactionReason:
        data = self._http.get(f"/api/v2/satisfaction_reasons/{int(reason_id)}")
        return to_domain(data=data["reason"], cls=SatisfactionReason)
