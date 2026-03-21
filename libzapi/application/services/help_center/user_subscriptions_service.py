from typing import Iterable
from libzapi.domain.models.help_center.user_subscription import UserSubscription
from libzapi.infrastructure.api_clients.help_center.user_subscription_api_client import UserSubscriptionApiClient


class UserSubscriptionsService:
    def __init__(self, client: UserSubscriptionApiClient) -> None:
        self._client = client

    def list_by_user(self, user_id: int) -> Iterable[UserSubscription]:
        return self._client.list_by_user(user_id=user_id)
