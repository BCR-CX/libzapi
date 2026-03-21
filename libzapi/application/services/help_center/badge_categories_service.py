from typing import Iterable
from libzapi.application.commands.help_center.badge_category_cmds import CreateBadgeCategoryCmd
from libzapi.domain.models.help_center.badge_category import BadgeCategory
from libzapi.infrastructure.api_clients.help_center.badge_category_api_client import BadgeCategoryApiClient


class BadgeCategoriesService:
    def __init__(self, client: BadgeCategoryApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[BadgeCategory]:
        return self._client.list_all()

    def get(self, badge_category_id: str) -> BadgeCategory:
        return self._client.get(badge_category_id=badge_category_id)

    def create(self, brand_id: int, name: str, slug: str) -> BadgeCategory:
        return self._client.create(cmd=CreateBadgeCategoryCmd(brand_id=brand_id, name=name, slug=slug))

    def delete(self, badge_category_id: str) -> None:
        self._client.delete(badge_category_id=badge_category_id)
