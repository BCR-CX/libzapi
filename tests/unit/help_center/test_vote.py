import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.vote import Vote
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import VoteApiClient
from hypothesis import given

strategy = builds(
    Vote,
    id=just(123),
)


@given(strategy)
def test_session_logical_key_from_id(model: Vote) -> None:
    assert model.logical_key.as_str() == "vote:id_123"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_article_votes", [100], "/api/v2/help_center/articles/100/votes", "votes"),
        ("list_post_votes", [100], "/api/v2/community/posts/100/votes", "votes"),
    ],
)
def test_vote_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = VoteApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_vote_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"vote": {}}
    mocker.patch("libzapi.infrastructure.api_clients.help_center.vote_api_client.to_domain", return_value=mocker.Mock())
    client = VoteApiClient(https)
    client.get(12345)
    https.get.assert_called_with("/api/v2/help_center/votes/12345")


@pytest.mark.parametrize(
    "method_name, args, expected_path",
    [
        ("up_article", [100], "/api/v2/help_center/articles/100/up"),
        ("down_article", [100], "/api/v2/help_center/articles/100/down"),
        ("up_post", [100], "/api/v2/community/posts/100/up"),
        ("down_post", [100], "/api/v2/community/posts/100/down"),
    ],
)
def test_vote_api_client_up_down(method_name, args, expected_path, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"vote": {}}
    mocker.patch("libzapi.infrastructure.api_clients.help_center.vote_api_client.to_domain", return_value=mocker.Mock())
    client = VoteApiClient(https)
    getattr(client, method_name)(*args)
    https.post.assert_called_with(expected_path, json={})


def test_vote_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = VoteApiClient(https)
    client.delete(12345)
    https.delete.assert_called_with("/api/v2/help_center/votes/12345")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_vote_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = VoteApiClient(https)
    with pytest.raises(error_cls):
        client.get(1)
