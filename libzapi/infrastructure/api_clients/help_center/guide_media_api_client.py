from __future__ import annotations
from typing import Iterator
from libzapi.domain.models.help_center.guide_media_object import Media
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class GuideMediaApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Media]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/guide/medias",
            base_url=self._http.base_url,
            items_key="guide_medias",
        ):
            yield to_domain(data=obj, cls=Media)

    def get(self, media_id: int) -> Media:
        data = self._http.get(f"/api/v2/guide/medias/{int(media_id)}")
        return to_domain(data=data["guide_media"], cls=Media)

    def create(self, file: tuple) -> Media:
        data = self._http.post_multipart("/api/v2/guide/medias", files={"file": file})
        return to_domain(data=data["guide_media"], cls=Media)

    def delete(self, media_id: int) -> None:
        self._http.delete(f"/api/v2/guide/medias/{int(media_id)}")
