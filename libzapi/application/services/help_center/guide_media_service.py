from typing import Iterable
from libzapi.domain.models.help_center.guide_media_object import Media
from libzapi.infrastructure.api_clients.help_center.guide_media_api_client import GuideMediaApiClient


class GuideMediaService:
    def __init__(self, client: GuideMediaApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Media]:
        return self._client.list_all()

    def get(self, media_id: int) -> Media:
        return self._client.get(media_id=media_id)

    def create(self, file: tuple) -> Media:
        return self._client.create(file=file)

    def delete(self, media_id: int) -> None:
        self._client.delete(media_id=media_id)
