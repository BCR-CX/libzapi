from typing import Iterable
from libzapi.application.commands.help_center.topic_cmds import CreateTopicCmd, UpdateTopicCmd
from libzapi.domain.models.help_center.topic import Topic
from libzapi.infrastructure.api_clients.help_center.topic_api_client import TopicApiClient


class TopicsService:
    def __init__(self, client: TopicApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Topic]:
        return self._client.list_all()

    def get(self, topic_id: int) -> Topic:
        return self._client.get(topic_id=topic_id)

    def create(
        self, name: str, description: str = "", position: int = 0, manageable_by=None, user_segment_id=None
    ) -> Topic:
        cmd = CreateTopicCmd(
            name=name,
            description=description,
            position=position,
            manageable_by=manageable_by,
            user_segment_id=user_segment_id,
        )
        return self._client.create(cmd=cmd)

    def update(
        self, topic_id: int, name=None, description=None, position=None, manageable_by=None, user_segment_id=None
    ) -> Topic:
        cmd = UpdateTopicCmd(
            name=name,
            description=description,
            position=position,
            manageable_by=manageable_by,
            user_segment_id=user_segment_id,
        )
        return self._client.update(topic_id=topic_id, cmd=cmd)

    def delete(self, topic_id: int) -> None:
        self._client.delete(topic_id=topic_id)
