from typing import Iterable
from libzapi.domain.models.help_center.theme import Theme
from libzapi.infrastructure.api_clients.help_center.theme_api_client import ThemeApiClient


class ThemesService:
    def __init__(self, client: ThemeApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Theme]:
        return self._client.list_all()

    def get(self, theme_id: str) -> Theme:
        return self._client.get(theme_id=theme_id)

    def publish(self, theme_id: str) -> Theme:
        return self._client.publish(theme_id=theme_id)

    def delete(self, theme_id: str) -> None:
        self._client.delete(theme_id=theme_id)
