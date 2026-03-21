import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.badge import Badge
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import BadgeApiClient
from hypothesis import given

strategy = builds(
    Badge,
    name=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Badge):
    assert model.logical_key.as_str() == "badge:cciia"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key", [("list_all", [], "/api/v2/gather/badges", "badges")]
)
def test_badge_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = BadgeApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_badge_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"badge": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_api_client.to_domain", return_value=mocker.Mock()
    )
    client = BadgeApiClient(https)
    client.get("abc123")
    https.get.assert_called_with("/api/v2/gather/badges/abc123")


def test_badge_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"badge": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_api_client.to_payload_create",
        return_value={"badge": {"name": "t"}},
    )
    client = BadgeApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/gather/badges", json={"badge": {"name": "t"}})


def test_badge_api_client_update(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"badge": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_api_client.to_payload_update",
        return_value={"badge": {"name": "u"}},
    )
    client = BadgeApiClient(https)
    client.update("abc123", mocker.Mock())
    https.put.assert_called_with("/api/v2/gather/badges/abc123", json={"badge": {"name": "u"}})


def test_badge_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = BadgeApiClient(https)
    client.delete("abc123")
    https.delete.assert_called_with("/api/v2/gather/badges/abc123")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_badge_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = BadgeApiClient(https)
    with pytest.raises(error_cls):
        client.get("1")
