from typing import Iterable
from libzapi.domain.models.help_center.vote import Vote
from libzapi.infrastructure.api_clients.help_center.vote_api_client import VoteApiClient


class VotesService:
    def __init__(self, client: VoteApiClient) -> None:
        self._client = client

    def list_article_votes(self, article_id: int) -> Iterable[Vote]:
        return self._client.list_article_votes(article_id=article_id)

    def list_post_votes(self, post_id: int) -> Iterable[Vote]:
        return self._client.list_post_votes(post_id=post_id)

    def list_article_comment_votes(self, article_id: int, comment_id: int) -> Iterable[Vote]:
        return self._client.list_article_comment_votes(article_id=article_id, comment_id=comment_id)

    def list_post_comment_votes(self, post_id: int, comment_id: int) -> Iterable[Vote]:
        return self._client.list_post_comment_votes(post_id=post_id, comment_id=comment_id)

    def up_article(self, article_id: int) -> Vote:
        return self._client.up_article(article_id=article_id)

    def down_article(self, article_id: int) -> Vote:
        return self._client.down_article(article_id=article_id)

    def up_post(self, post_id: int) -> Vote:
        return self._client.up_post(post_id=post_id)

    def down_post(self, post_id: int) -> Vote:
        return self._client.down_post(post_id=post_id)

    def up_article_comment(self, article_id: int, comment_id: int) -> Vote:
        return self._client.up_article_comment(article_id=article_id, comment_id=comment_id)

    def down_article_comment(self, article_id: int, comment_id: int) -> Vote:
        return self._client.down_article_comment(article_id=article_id, comment_id=comment_id)

    def up_post_comment(self, post_id: int, comment_id: int) -> Vote:
        return self._client.up_post_comment(post_id=post_id, comment_id=comment_id)

    def down_post_comment(self, post_id: int, comment_id: int) -> Vote:
        return self._client.down_post_comment(post_id=post_id, comment_id=comment_id)

    def get(self, vote_id: int) -> Vote:
        return self._client.get(vote_id=vote_id)

    def delete(self, vote_id: int) -> None:
        self._client.delete(vote_id=vote_id)
