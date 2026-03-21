import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.post import Post
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import PostApiClient
from hypothesis import given

strategy = builds(
    Post,
    title=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Post):
    assert model.logical_key.as_str() == "post:cciia"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/community/posts", "posts"),
        ("list_by_topic", [100], "/api/v2/community/topics/100/posts", "posts"),
        ("list_by_user", [200], "/api/v2/community/users/200/posts", "posts"),
    ],
)
def test_post_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = PostApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_post_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"post": {}}
    mocker.patch("libzapi.infrastructure.api_clients.help_center.post_api_client.to_domain", return_value=mocker.Mock())
    client = PostApiClient(https)
    client.get(12345)
    https.get.assert_called_with("/api/v2/community/posts/12345")


def test_post_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"post": {}}
    mocker.patch("libzapi.infrastructure.api_clients.help_center.post_api_client.to_domain", return_value=mocker.Mock())
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.post_api_client.to_payload_create",
        return_value={"post": {"title": "t"}},
    )
    client = PostApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/community/posts", json={"post": {"title": "t"}})


def test_post_api_client_update(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"post": {}}
    mocker.patch("libzapi.infrastructure.api_clients.help_center.post_api_client.to_domain", return_value=mocker.Mock())
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.post_api_client.to_payload_update",
        return_value={"post": {"title": "u"}},
    )
    client = PostApiClient(https)
    client.update(12345, mocker.Mock())
    https.put.assert_called_with("/api/v2/community/posts/12345", json={"post": {"title": "u"}})


def test_post_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = PostApiClient(https)
    client.delete(12345)
    https.delete.assert_called_with("/api/v2/community/posts/12345")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_post_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = PostApiClient(https)
    with pytest.raises(error_cls):
        client.get(1)
