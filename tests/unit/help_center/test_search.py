import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import SearchApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("search_articles", ["test"], "/api/v2/help_center/articles/search?query=test", "results"),
        ("search_posts", ["test"], "/api/v2/help_center/community_posts/search?query=test", "results"),
    ],
)
def test_search_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = SearchApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_search_articles_with_params(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"results": []}
    client = SearchApiClient(https)
    list(client.search_articles("test", locale="en-us"))
    https.get.assert_called_with("/api/v2/help_center/articles/search?query=test&locale=en-us")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_search_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = SearchApiClient(https)
    with pytest.raises(error_cls):
        list(client.search_articles("test"))
