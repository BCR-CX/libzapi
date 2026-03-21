from typing import Iterable
from libzapi.application.commands.help_center.content_subscription_cmds import CreateContentSubscriptionCmd
from libzapi.domain.models.help_center.content_subscription import ContentSubscription
from libzapi.infrastructure.api_clients.help_center.content_subscription_api_client import ContentSubscriptionApiClient


class ContentSubscriptionsService:
    def __init__(self, client: ContentSubscriptionApiClient) -> None:
        self._client = client

    def list(self, content_type: str, content_id: int) -> Iterable[ContentSubscription]:
        return self._client.list(content_type=content_type, content_id=content_id)

    def get(self, content_type: str, content_id: int, subscription_id: int) -> ContentSubscription:
        return self._client.get(content_type=content_type, content_id=content_id, subscription_id=subscription_id)

    def create(self, content_type: str, content_id: int, locale: str = "") -> ContentSubscription:
        return self._client.create(
            content_type=content_type, content_id=content_id, cmd=CreateContentSubscriptionCmd(locale=locale)
        )

    def delete(self, content_type: str, content_id: int, subscription_id: int) -> None:
        self._client.delete(content_type=content_type, content_id=content_id, subscription_id=subscription_id)
