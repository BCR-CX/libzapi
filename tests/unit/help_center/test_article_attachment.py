import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.article_attachment import ArticleAttachment
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ArticleAttachmentApiClient
from hypothesis import given

strategy = builds(ArticleAttachment, file_name=just("cciiA.csv"))


@given(strategy)
def test_session_logical_key_from_id(model: ArticleAttachment):
    assert model.logical_key.as_str() == "article_attachment:cciia.csv"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [999], "/api/v2/help_center/articles/999/attachments", "article_attachments"),
        ("list_inline", [999], "/api/v2/help_center/articles/999/attachments/inline", "article_attachments"),
        ("list_block", [999], "/api/v2/help_center/articles/999/attachments/block", "article_attachments"),
    ],
)
def test_article_attachment_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = ArticleAttachmentApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_article_attachment_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"article_attachment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_attachment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    client = ArticleAttachmentApiClient(https)
    client.get(12345)
    https.get.assert_called_with("/api/v2/help_center/articles/attachments/12345")


def test_article_attachment_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post_multipart.return_value = {"article_attachment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.article_attachment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    client = ArticleAttachmentApiClient(https)
    client.create(999, file=("test.png", b"data", "image/png"))
    https.post_multipart.assert_called_with(
        "/api/v2/help_center/articles/999/attachments", files={"file": ("test.png", b"data", "image/png")}, data=None
    )


def test_article_attachment_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = ArticleAttachmentApiClient(https)
    client.delete(12345)
    https.delete.assert_called_with("/api/v2/help_center/articles/attachments/12345")


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
        client.get(1)
