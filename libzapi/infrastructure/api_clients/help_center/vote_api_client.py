from __future__ import annotations
from typing import Iterator
from libzapi.domain.models.help_center.vote import Vote
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class VoteApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_article_votes(self, article_id: int) -> Iterator[Vote]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/{int(article_id)}/votes",
            base_url=self._http.base_url,
            items_key="votes",
        ):
            yield to_domain(data=obj, cls=Vote)

    def list_post_votes(self, post_id: int) -> Iterator[Vote]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/community/posts/{int(post_id)}/votes",
            base_url=self._http.base_url,
            items_key="votes",
        ):
            yield to_domain(data=obj, cls=Vote)

    def list_article_comment_votes(self, article_id: int, comment_id: int) -> Iterator[Vote]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/{int(article_id)}/comments/{int(comment_id)}/votes",
            base_url=self._http.base_url,
            items_key="votes",
        ):
            yield to_domain(data=obj, cls=Vote)

    def list_post_comment_votes(self, post_id: int, comment_id: int) -> Iterator[Vote]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/community/posts/{int(post_id)}/comments/{int(comment_id)}/votes",
            base_url=self._http.base_url,
            items_key="votes",
        ):
            yield to_domain(data=obj, cls=Vote)

    def up_article(self, article_id: int) -> Vote:
        data = self._http.post(f"/api/v2/help_center/articles/{int(article_id)}/up", json={})
        return to_domain(data=data["vote"], cls=Vote)

    def down_article(self, article_id: int) -> Vote:
        data = self._http.post(f"/api/v2/help_center/articles/{int(article_id)}/down", json={})
        return to_domain(data=data["vote"], cls=Vote)

    def up_article_comment(self, article_id: int, comment_id: int) -> Vote:
        data = self._http.post(f"/api/v2/help_center/articles/{int(article_id)}/comments/{int(comment_id)}/up", json={})
        return to_domain(data=data["vote"], cls=Vote)

    def down_article_comment(self, article_id: int, comment_id: int) -> Vote:
        data = self._http.post(
            f"/api/v2/help_center/articles/{int(article_id)}/comments/{int(comment_id)}/down", json={}
        )
        return to_domain(data=data["vote"], cls=Vote)

    def up_post(self, post_id: int) -> Vote:
        data = self._http.post(f"/api/v2/community/posts/{int(post_id)}/up", json={})
        return to_domain(data=data["vote"], cls=Vote)

    def down_post(self, post_id: int) -> Vote:
        data = self._http.post(f"/api/v2/community/posts/{int(post_id)}/down", json={})
        return to_domain(data=data["vote"], cls=Vote)

    def up_post_comment(self, post_id: int, comment_id: int) -> Vote:
        data = self._http.post(f"/api/v2/community/posts/{int(post_id)}/comments/{int(comment_id)}/up", json={})
        return to_domain(data=data["vote"], cls=Vote)

    def down_post_comment(self, post_id: int, comment_id: int) -> Vote:
        data = self._http.post(f"/api/v2/community/posts/{int(post_id)}/comments/{int(comment_id)}/down", json={})
        return to_domain(data=data["vote"], cls=Vote)

    def get(self, vote_id: int) -> Vote:
        data = self._http.get(f"/api/v2/help_center/votes/{int(vote_id)}")
        return to_domain(data=data["vote"], cls=Vote)

    def delete(self, vote_id: int) -> None:
        self._http.delete(f"/api/v2/help_center/votes/{int(vote_id)}")
