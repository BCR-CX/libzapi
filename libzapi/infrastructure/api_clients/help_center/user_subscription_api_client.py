from __future__ import annotations
from typing import Iterator
from libzapi.domain.models.help_center.user_subscription import UserSubscription
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class UserSubscriptionApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_by_user(self, user_id: int) -> Iterator[UserSubscription]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/users/{int(user_id)}/subscriptions",
            base_url=self._http.base_url,
            items_key="subscriptions",
        ):
            yield to_domain(data=obj, cls=UserSubscription)
