import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.post_comment import PostComment
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import PostCommentApiClient
from hypothesis import given

strategy = builds(
    PostComment,
    id=just(333),
)


@given(strategy)
def test_session_logical_key_from_id(model: PostComment):
    assert model.logical_key.as_str() == "post_comment:id_333"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_by_post", [100], "/api/v2/community/posts/100/comments", "comments"),
        ("list_by_user", [200], "/api/v2/community/users/200/comments", "comments"),
    ],
)
def test_post_comment_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = PostCommentApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_post_comment_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"comment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.post_comment_api_client.to_domain", return_value=mocker.Mock()
    )
    client = PostCommentApiClient(https)
    client.get(100, 200)
    https.get.assert_called_with("/api/v2/community/posts/100/comments/200")


def test_post_comment_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"comment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.post_comment_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.post_comment_api_client.to_payload_create",
        return_value={"comment": {"body": "t"}},
    )
    client = PostCommentApiClient(https)
    client.create(100, mocker.Mock())
    https.post.assert_called_with("/api/v2/community/posts/100/comments", json={"comment": {"body": "t"}})


def test_post_comment_api_client_update(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"comment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.post_comment_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.post_comment_api_client.to_payload_update",
        return_value={"comment": {"body": "u"}},
    )
    client = PostCommentApiClient(https)
    client.update(100, 200, mocker.Mock())
    https.put.assert_called_with("/api/v2/community/posts/100/comments/200", json={"comment": {"body": "u"}})


def test_post_comment_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = PostCommentApiClient(https)
    client.delete(100, 200)
    https.delete.assert_called_with("/api/v2/community/posts/100/comments/200")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_post_comment_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = PostCommentApiClient(https)
    with pytest.raises(error_cls):
        client.get(1, 1)
