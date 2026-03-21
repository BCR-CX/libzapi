import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.content_subscription import ContentSubscription
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ContentSubscriptionApiClient
from hypothesis import given

strategy = builds(
    ContentSubscription,
    id=just("555"),
)


@given(strategy)
def test_session_logical_key_from_id(model: ContentSubscription):
    assert model.logical_key.as_str() == "content_subscription:id_555"


@pytest.mark.parametrize(
    "content_type, expected_prefix",
    [
        ("articles", "/api/v2/help_center/articles"),
        ("sections", "/api/v2/help_center/sections"),
        ("topics", "/api/v2/community/topics"),
        ("posts", "/api/v2/community/posts"),
    ],
)
def test_content_subscription_api_client_list(content_type, expected_prefix, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"subscriptions": []}
    client = ContentSubscriptionApiClient(https)
    list(client.list(content_type, 100))
    https.get.assert_called_with(f"{expected_prefix}/100/subscriptions")


def test_content_subscription_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"subscription": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.content_subscription_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    client = ContentSubscriptionApiClient(https)
    client.get("articles", 100, 200)
    https.get.assert_called_with("/api/v2/help_center/articles/100/subscriptions/200")


def test_content_subscription_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"subscription": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.content_subscription_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.content_subscription_api_client.to_payload_create",
        return_value={"subscription": {"locale": "en-us"}},
    )
    client = ContentSubscriptionApiClient(https)
    client.create("articles", 100, mocker.Mock())
    https.post.assert_called_with(
        "/api/v2/help_center/articles/100/subscriptions", json={"subscription": {"locale": "en-us"}}
    )


def test_content_subscription_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = ContentSubscriptionApiClient(https)
    client.delete("articles", 100, 200)
    https.delete.assert_called_with("/api/v2/help_center/articles/100/subscriptions/200")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_content_subscription_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = ContentSubscriptionApiClient(https)
    with pytest.raises(error_cls):
        client.get("articles", 1, 1)
