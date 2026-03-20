import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.article_attachment import ArticleAttachment
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ArticleAttachmentApiClient
from hypothesis import given

strategy = builds(
    ArticleAttachment,
    file_name=just("cciiA.csv"),
)


@given(strategy)
def test_session_logical_key_from_id(model: ArticleAttachment):
    assert model.logical_key.as_str() == "article_attachment:cciia.csv"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_inline", [999], "/api/v2/help_center/articles/999/attachments/inline", "article_attachments"),
    ],
)
def test_article_attachment_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}

    client = ArticleAttachmentApiClient(https)
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
def test_article_attachment_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = ArticleAttachmentApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_inline(999))
