from __future__ import annotations

from libzapi.domain.models.agent_availability.account_group_availability import AccountGroupAvailability
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/account_groups/availability"


class AccountGroupAvailabilityApiClient:
    """HTTP adapter for Zendesk Account Groups Availability."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, group_id: int) -> AccountGroupAvailability:
        data = self._http.get(f"{_BASE}/{int(group_id)}")
        return to_domain(data=data, cls=AccountGroupAvailability)
