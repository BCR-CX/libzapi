import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.theme import Theme
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import ThemeApiClient
from hypothesis import given

strategy = builds(
    Theme,
    name=just("cciiA"),
    version=just("1.0.0"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Theme):
    assert model.logical_key.as_str() == "theme:v_1.0.0_cciia"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key", [("list_all", [], "/api/v2/guide/theming/themes", "themes")]
)
def test_theme_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = ThemeApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_theme_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"theme": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.theme_api_client.to_domain", return_value=mocker.Mock()
    )
    client = ThemeApiClient(https)
    client.get("abc123")
    https.get.assert_called_with("/api/v2/guide/theming/themes/abc123")


def test_theme_api_client_publish(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"theme": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.theme_api_client.to_domain", return_value=mocker.Mock()
    )
    client = ThemeApiClient(https)
    client.publish("abc123")
    https.post.assert_called_with("/api/v2/guide/theming/themes/abc123/publish", json={})


def test_theme_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = ThemeApiClient(https)
    client.delete("abc123")
    https.delete.assert_called_with("/api/v2/guide/theming/themes/abc123")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_theme_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = ThemeApiClient(https)
    with pytest.raises(error_cls):
        client.get("1")
