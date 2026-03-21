import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.user_subscription import UserSubscription
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import UserSubscriptionApiClient
from hypothesis import given

strategy = builds(
    UserSubscription,
    id=just(2111),
)


@given(strategy)
def test_session_logical_key_from_id(model: UserSubscription):
    assert model.logical_key.as_str() == "user_subscription:id_2111"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [("list_by_user", [100], "/api/v2/help_center/users/100/subscriptions", "subscriptions")],
)
def test_user_subscription_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = UserSubscriptionApiClient(https)
    list(getattr(client, method_name)(*args))
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
def test_user_subscription_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = UserSubscriptionApiClient(https)
    with pytest.raises(error_cls):
        list(client.list_by_user(1))
