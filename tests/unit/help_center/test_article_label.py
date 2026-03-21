import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.article_label import ArticleLabel
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ArticleLabelApiClient
from hypothesis import given

strategy = builds(
    ArticleLabel,
    name=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: ArticleLabel):
    assert model.logical_key.as_str() == "article_label:cciia"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/help_center/articles/labels", "labels"),
        ("list_by_article", [100], "/api/v2/help_center/articles/100/labels", "labels"),
    ],
)
def test_article_label_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}

    client = ArticleLabelApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_article_label_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"label": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_label_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = ArticleLabelApiClient(https)
    client.get(100, 200)

    https.get.assert_called_with("/api/v2/help_center/articles/100/labels/200")


def test_article_label_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"label": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_label_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_label_api_client.to_payload_create",
        return_value={"label": {"name": "test"}},
    )

    client = ArticleLabelApiClient(https)
    cmd = mocker.Mock()
    client.create(100, cmd)

    https.post.assert_called_with(
        "/api/v2/help_center/articles/100/labels",
        json={"label": {"name": "test"}},
    )


def test_article_label_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = ArticleLabelApiClient(https)
    client.delete(100, 200)

    https.delete.assert_called_with("/api/v2/help_center/articles/100/labels/200")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_article_label_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = ArticleLabelApiClient(https)

    with pytest.raises(error_cls):
        client.get(1, 1)
