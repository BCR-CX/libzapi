import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.badge_category import BadgeCategory
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import BadgeCategoryApiClient
from hypothesis import given

strategy = builds(
    BadgeCategory,
    name=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: BadgeCategory):
    assert model.logical_key.as_str() == "badge_category:cciia"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [("list_all", [], "/api/v2/gather/badge_categories", "badge_categories")],
)
def test_badge_category_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = BadgeCategoryApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_badge_category_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"badge_category": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_category_api_client.to_domain", return_value=mocker.Mock()
    )
    client = BadgeCategoryApiClient(https)
    client.get(12345)
    https.get.assert_called_with("/api/v2/gather/badge_categories/12345")


def test_badge_category_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"badge_category": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_category_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_category_api_client.to_payload_create",
        return_value={"badge_category": {"name": "t"}},
    )
    client = BadgeCategoryApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/gather/badge_categories", json={"badge_category": {"name": "t"}})


def test_badge_category_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = BadgeCategoryApiClient(https)
    client.delete(12345)
    https.delete.assert_called_with("/api/v2/gather/badge_categories/12345")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_badge_category_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = BadgeCategoryApiClient(https)
    with pytest.raises(error_cls):
        client.get(1)
