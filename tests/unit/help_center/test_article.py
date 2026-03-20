import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.article import Article
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ArticleApiClient
from hypothesis import given

strategy = builds(
    Article,
    title=just("art123"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Article):
    assert model.logical_key.as_str() == "article:art123"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/help_center/articles", "articles"),
        ("list_all_by_locale", ["en-us"], "/api/v2/help_center/en-us/articles", "articles"),
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
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


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
        list(client.list_all())
