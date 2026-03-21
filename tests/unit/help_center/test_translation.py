import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.translation import Translation
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import TranslationApiClient
from hypothesis import given

strategy = builds(
    Translation,
    title=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Translation) -> None:
    assert model.logical_key.as_str() == "translation:cciia"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list", ["articles", 100], "/api/v2/help_center/articles/100/translations", "translations"),
        ("list", ["sections", 200], "/api/v2/help_center/sections/200/translations", "translations"),
    ],
)
def test_translation_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}

    client = TranslationApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_translation_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"translation": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.translation_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = TranslationApiClient(https)
    client.get("articles", 100, "en-us")

    https.get.assert_called_with("/api/v2/help_center/articles/100/translations/en-us")


def test_translation_api_client_list_missing(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"locales": ["fr", "de"]}

    client = TranslationApiClient(https)
    result = client.list_missing("articles", 100)

    https.get.assert_called_with("/api/v2/help_center/articles/100/translations/missing")
    assert result == ["fr", "de"]


def test_translation_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"translation": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.translation_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.translation_api_client.to_payload_create",
        return_value={"translation": {"locale": "fr"}},
    )

    client = TranslationApiClient(https)
    cmd = mocker.Mock()
    client.create("articles", 100, cmd)

    https.post.assert_called_with(
        "/api/v2/help_center/articles/100/translations",
        json={"translation": {"locale": "fr"}},
    )


def test_translation_api_client_update(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"translation": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.translation_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.translation_api_client.to_payload_update",
        return_value={"translation": {"title": "updated"}},
    )

    client = TranslationApiClient(https)
    cmd = mocker.Mock()
    client.update("articles", 100, "fr", cmd)

    https.put.assert_called_with(
        "/api/v2/help_center/articles/100/translations/fr",
        json={"translation": {"title": "updated"}},
    )


def test_translation_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = TranslationApiClient(https)
    client.delete(12345)

    https.delete.assert_called_with("/api/v2/help_center/translations/12345")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_translation_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = TranslationApiClient(https)

    with pytest.raises(error_cls):
        client.get("articles", 1, "en-us")
