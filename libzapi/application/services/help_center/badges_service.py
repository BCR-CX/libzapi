from typing import Iterable
from libzapi.application.commands.help_center.badge_cmds import CreateBadgeCmd, UpdateBadgeCmd
from libzapi.domain.models.help_center.badge import Badge
from libzapi.infrastructure.api_clients.help_center.badge_api_client import BadgeApiClient


class BadgesService:
    def __init__(self, client: BadgeApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Badge]:
        return self._client.list_all()

    def get(self, badge_id: str) -> Badge:
        return self._client.get(badge_id=badge_id)

    def create(self, badge_category_id: str, name: str, description: str = "") -> Badge:
        return self._client.create(
            cmd=CreateBadgeCmd(badge_category_id=badge_category_id, name=name, description=description)
        )

    def update(self, badge_id: str, name=None, description=None, badge_category_id=None) -> Badge:
        return self._client.update(
            badge_id=badge_id,
            cmd=UpdateBadgeCmd(name=name, description=description, badge_category_id=badge_category_id),
        )

    def delete(self, badge_id: str) -> None:
        self._client.delete(badge_id=badge_id)
