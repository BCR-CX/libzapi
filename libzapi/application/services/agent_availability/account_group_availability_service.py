from libzapi.domain.models.agent_availability.account_group_availability import AccountGroupAvailability
from libzapi.infrastructure.api_clients.agent_availability import AccountGroupAvailabilityApiClient


class AccountGroupAvailabilityService:
    """High-level service using the API client."""

    def __init__(self, client: AccountGroupAvailabilityApiClient) -> None:
        self._client = client

    def get(self, group_id: int) -> AccountGroupAvailability:
        return self._client.get(group_id=group_id)
