import pytest

from libzapi.infrastructure.api_clients.ticketing.session_api_client import (
    SessionApiClient,
)


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.session_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.session_api_client.yield_items"
    )


def test_list_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}])
    client = SessionApiClient(http)
    result = list(client.list())
    assert result[0]["_cls"] == "Session"
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/sessions"
    assert kwargs["items_key"] == "sessions"


def test_list_user_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}])
    client = SessionApiClient(http)
    result = list(client.list_user(user_id=5))
    assert result[0]["_cls"] == "Session"
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/users/5/sessions"


def test_get_reads_session_key(http, domain):
    http.get.return_value = {"session": {"id": 7}}
    client = SessionApiClient(http)
    result = client.get(user_id=5, session_id=7)
    http.get.assert_called_with("/api/v2/users/5/sessions/7")
    assert result["_cls"] == "Session"


def test_delete_calls_delete(http):
    client = SessionApiClient(http)
    client.delete(user_id=5, session_id=7)
    http.delete.assert_called_with("/api/v2/users/5/sessions/7")


def test_delete_user_sessions_calls_delete(http):
    client = SessionApiClient(http)
    client.delete_user_sessions(user_id=5)
    http.delete.assert_called_with("/api/v2/users/5/sessions")


def test_get_current_reads_session_key(http, domain):
    http.get.return_value = {"session": {"id": 9}}
    client = SessionApiClient(http)
    result = client.get_current()
    http.get.assert_called_with("/api/v2/users/me/session")
    assert result["_cls"] == "Session"


def test_logout_current_calls_delete(http):
    client = SessionApiClient(http)
    client.logout_current()
    http.delete.assert_called_with("/api/v2/users/me/logout")
