import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized
from libzapi.infrastructure.api_clients.ticketing import LocaleApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.locale_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.mark.parametrize(
    "method, path",
    [
        ("list_all", "/api/v2/locales"),
        ("list_agent", "/api/v2/locales/agent"),
        ("list_public", "/api/v2/locales/public"),
    ],
)
def test_list_endpoints_hit_expected_path(method, path, http, domain):
    http.get.return_value = {"locales": [{"id": 1}]}
    client = LocaleApiClient(http)
    items = list(getattr(client, method)())
    assert len(items) == 1
    assert items[0]["_cls"] == "Locale"
    http.get.assert_called_with(path)


def test_get_by_id(http, domain):
    http.get.return_value = {"locale": {"id": 1}}
    client = LocaleApiClient(http)
    result = client.get(1)
    assert result["_cls"] == "Locale"
    http.get.assert_called_with("/api/v2/locales/1")


def test_get_by_code(http, domain):
    http.get.return_value = {"locale": {"id": 1}}
    client = LocaleApiClient(http)
    result = client.get("en-US")
    assert result["_cls"] == "Locale"
    http.get.assert_called_with("/api/v2/locales/en-US")


def test_get_current(http, domain):
    http.get.return_value = {"locale": {"id": 1}}
    client = LocaleApiClient(http)
    result = client.get_current()
    assert result["_cls"] == "Locale"
    http.get.assert_called_with("/api/v2/locales/current")


def test_detect_best(http, domain):
    http.get.return_value = {"locale": {"id": 1}}
    client = LocaleApiClient(http)
    result = client.detect_best(["en-US", "pt-BR"])
    assert result["_cls"] == "Locale"
    http.get.assert_called_with(
        "/api/v2/locales/detect_best_locale?available=en-US%2Cpt-BR"
    )


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, RateLimited])
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = LocaleApiClient(http)
    with pytest.raises(error_cls):
        list(client.list_all())


def test_locale_logical_key():
    from libzapi.domain.models.ticketing.locale import Locale

    locale = Locale(id=1, locale="en-US", name="English (US)")
    assert locale.logical_key.as_str() == "locale:en_us"
