import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.article_comment import ArticleComment
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ArticleCommentApiClient
from hypothesis import given

strategy = builds(
    ArticleComment,
    id=just(123),
)


@given(strategy)
def test_session_logical_key_from_id(model: ArticleComment):
    assert model.logical_key.as_str() == "article_comment:id_123"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_by_article", [100], "/api/v2/help_center/articles/100/comments", "comments"),
        ("list_by_user", [200], "/api/v2/help_center/users/200/comments", "comments"),
    ],
)
def test_article_comment_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = ArticleCommentApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_article_comment_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"comment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_comment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    client = ArticleCommentApiClient(https)
    client.get(100, 200)
    https.get.assert_called_with("/api/v2/help_center/articles/100/comments/200")


def test_article_comment_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"comment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_comment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_comment_api_client.to_payload_create",
        return_value={"comment": {"body": "test"}},
    )
    client = ArticleCommentApiClient(https)
    client.create(100, mocker.Mock())
    https.post.assert_called_with("/api/v2/help_center/articles/100/comments", json={"comment": {"body": "test"}})


def test_article_comment_api_client_update(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"comment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_comment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_comment_api_client.to_payload_update",
        return_value={"comment": {"body": "u"}},
    )
    client = ArticleCommentApiClient(https)
    client.update(100, 200, mocker.Mock())
    https.put.assert_called_with("/api/v2/help_center/articles/100/comments/200", json={"comment": {"body": "u"}})


def test_article_comment_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = ArticleCommentApiClient(https)
    client.delete(100, 200)
    https.delete.assert_called_with("/api/v2/help_center/articles/100/comments/200")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_article_comment_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = ArticleCommentApiClient(https)
    with pytest.raises(error_cls):
        client.get(1, 1)
