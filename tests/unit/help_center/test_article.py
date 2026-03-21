import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.article import Article
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ArticleApiClient
from hypothesis import given

strategy = builds(Article, title=just("art123"))


@given(strategy)
def test_session_logical_key_from_id(model: Article):
    assert model.logical_key.as_str() == "article:art123"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/help_center/articles", "articles"),
        ("list_all_by_locale", ["en-us"], "/api/v2/help_center/en-us/articles", "articles"),
        ("list_by_category", [100], "/api/v2/help_center/categories/100/articles", "articles"),
        ("list_by_section", [200], "/api/v2/help_center/sections/200/articles", "articles"),
        ("list_by_user", [300], "/api/v2/help_center/users/300/articles", "articles"),
        (
            "list_incremental",
            [1609459200],
            "/api/v2/help_center/articles/incremental?start_time=1609459200",
            "articles",
        ),
    ],
)
def test_article_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = ArticleApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_article_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"article": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_api_client.to_domain", return_value=mocker.Mock()
    )
    client = ArticleApiClient(https)
    client.get(12345)
    https.get.assert_called_with("/api/v2/help_center/articles/12345")


def test_article_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"article": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_api_client.to_payload_create",
        return_value={"article": {"title": "t"}},
    )
    client = ArticleApiClient(https)
    client.create(999, mocker.Mock())
    https.post.assert_called_with("/api/v2/help_center/sections/999/articles", json={"article": {"title": "t"}})


def test_article_api_client_update(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"article": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_api_client.to_payload_update",
        return_value={"article": {"title": "u"}},
    )
    client = ArticleApiClient(https)
    client.update(12345, mocker.Mock())
    https.put.assert_called_with("/api/v2/help_center/articles/12345", json={"article": {"title": "u"}})


def test_article_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = ArticleApiClient(https)
    client.delete(12345)
    https.delete.assert_called_with("/api/v2/help_center/articles/12345")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_article_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = ArticleApiClient(https)
    with pytest.raises(error_cls):
        client.get(1)
