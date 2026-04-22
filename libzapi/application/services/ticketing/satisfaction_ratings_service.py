from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.satisfaction_rating_cmds import (
    CreateSatisfactionRatingCmd,
)
from libzapi.domain.models.ticketing.satisfaction_rating import (
    SatisfactionRating,
    SatisfactionReason,
)
from libzapi.infrastructure.api_clients.ticketing.satisfaction_rating_api_client import (
    SatisfactionRatingApiClient,
)


class SatisfactionRatingsService:
    """High-level service for Zendesk Satisfaction Ratings + Reasons."""

    def __init__(self, client: SatisfactionRatingApiClient) -> None:
        self._client = client

    def list_all(
        self,
        *,
        score: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> Iterable[SatisfactionRating]:
        return self._client.list(score=score, start_time=start_time, end_time=end_time)

    def list_received(self) -> Iterable[SatisfactionRating]:
        return self._client.list_received()

    def get_by_id(self, rating_id: int) -> SatisfactionRating:
        return self._client.get(rating_id=rating_id)

    def create_for_ticket(
        self,
        ticket_id: int,
        score: str,
        comment: str | None = None,
        reason_id: int | None = None,
    ) -> SatisfactionRating:
        return self._client.create_for_ticket(
            ticket_id=ticket_id,
            entity=CreateSatisfactionRatingCmd(
                score=score, comment=comment, reason_id=reason_id
            ),
        )

    def list_reasons(self) -> Iterable[SatisfactionReason]:
        return self._client.list_reasons()

    def get_reason(self, reason_id: int) -> SatisfactionReason:
        return self._client.get_reason(reason_id=reason_id)
