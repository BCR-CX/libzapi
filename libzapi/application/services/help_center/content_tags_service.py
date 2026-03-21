from typing import Iterable
from libzapi.application.commands.help_center.content_tag_cmds import CreateContentTagCmd, UpdateContentTagCmd
from libzapi.domain.models.help_center.content_tag import ContentTag
from libzapi.infrastructure.api_clients.help_center.content_tag_api_client import ContentTagApiClient


class ContentTagsService:
    def __init__(self, client: ContentTagApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[ContentTag]:
        return self._client.list_all()

    def get(self, content_tag_id: str) -> ContentTag:
        return self._client.get(content_tag_id=content_tag_id)

    def create(self, name: str) -> ContentTag:
        return self._client.create(cmd=CreateContentTagCmd(name=name))

    def update(self, content_tag_id: str, name=None) -> ContentTag:
        return self._client.update(content_tag_id=content_tag_id, cmd=UpdateContentTagCmd(name=name))

    def delete(self, content_tag_id: str) -> None:
        self._client.delete(content_tag_id=content_tag_id)
