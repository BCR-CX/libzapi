from http.client import RemoteDisconnected
from unittest.mock import Mock

import pytest
import requests

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.http.client import HttpClient


def _make_response(status_code: int, text: str = "", json_data: dict | None = None) -> Mock:
    resp = Mock(spec=requests.Response)
    resp.status_code = status_code
    resp.text = text
    if json_data is not None:
        resp.json.return_value = json_data
    return resp


# ---------------------------------------------------------------------------
# _raise: domain error mapping
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("status_code", "exc_class"),
    [
        (401, Unauthorized),
        (404, NotFound),
        (422, UnprocessableEntity),
        (429, RateLimited),
    ],
)
def test_raise_maps_status_to_domain_error(status_code, exc_class):
    resp = _make_response(status_code, text=f"error for {status_code}")
    with pytest.raises(exc_class, match=f"error for {status_code}"):
        HttpClient._raise(resp)


# ---------------------------------------------------------------------------
# _raise: 5xx delegates to raise_for_status
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status_code", [500, 502, 503, 504])
def test_raise_5xx_calls_raise_for_status(status_code):
    resp = _make_response(status_code)
    resp.raise_for_status.side_effect = requests.HTTPError(f"{status_code} Server Error")
    with pytest.raises(requests.HTTPError, match=f"{status_code} Server Error"):
        HttpClient._raise(resp)
    resp.raise_for_status.assert_called_once()


# ---------------------------------------------------------------------------
# _raise: 200 OK is a no-op
# ---------------------------------------------------------------------------


def test_raise_200_does_nothing():
    resp = _make_response(200)
    HttpClient._raise(resp)  # should not raise any exception


# ---------------------------------------------------------------------------
# GET
# ---------------------------------------------------------------------------


def test_get_returns_json(mocker):
    client = HttpClient("https://example.zendesk.com/", headers={"Authorization": "Bearer tok"})
    resp = _make_response(200, json_data={"ticket": {"id": 1}})
    mocker.patch.object(client.session, "request", return_value=resp)

    result = client.get("/api/v2/tickets/1.json")

    client.session.request.assert_called_once_with(
        "GET", "https://example.zendesk.com/api/v2/tickets/1.json", params=None, timeout=30.0
    )
    assert result == {"ticket": {"id": 1}}


def test_get_raises_on_error(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(404, text="Not Found")
    mocker.patch.object(client.session, "request", return_value=resp)

    with pytest.raises(NotFound, match="Not Found"):
        client.get("/api/v2/tickets/999.json")


# ---------------------------------------------------------------------------
# POST
# ---------------------------------------------------------------------------


def test_post_sends_json_and_returns_response(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    payload = {"ticket": {"subject": "Help"}}
    resp = _make_response(201, json_data={"ticket": {"id": 42, "subject": "Help"}})
    mocker.patch.object(client.session, "request", return_value=resp)

    result = client.post("/api/v2/tickets.json", json=payload)

    client.session.request.assert_called_once_with(
        "POST", "https://example.zendesk.com/api/v2/tickets.json", json=payload, timeout=30.0
    )
    assert result == {"ticket": {"id": 42, "subject": "Help"}}


def test_post_raises_on_error(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(401, text="Invalid credentials")
    mocker.patch.object(client.session, "request", return_value=resp)

    with pytest.raises(Unauthorized, match="Invalid credentials"):
        client.post("/api/v2/tickets.json", json={})


# ---------------------------------------------------------------------------
# PUT
# ---------------------------------------------------------------------------


def test_put_sends_json_and_returns_response(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    payload = {"ticket": {"status": "solved"}}
    resp = _make_response(200, json_data={"ticket": {"id": 1, "status": "solved"}})
    mocker.patch.object(client.session, "request", return_value=resp)

    result = client.put("/api/v2/tickets/1.json", json=payload)

    client.session.request.assert_called_once_with(
        "PUT", "https://example.zendesk.com/api/v2/tickets/1.json", json=payload, timeout=30.0
    )
    assert result == {"ticket": {"id": 1, "status": "solved"}}


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------


def test_delete_returns_none(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(204)
    mocker.patch.object(client.session, "request", return_value=resp)

    result = client.delete("/api/v2/tickets/1.json")

    client.session.request.assert_called_once_with(
        "DELETE", "https://example.zendesk.com/api/v2/tickets/1.json", json=None, timeout=30.0
    )
    assert result is None


def test_delete_does_not_call_json(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(204)
    mocker.patch.object(client.session, "request", return_value=resp)

    client.delete("/api/v2/tickets/1.json")

    resp.json.assert_not_called()


# ---------------------------------------------------------------------------
# Constructor
# ---------------------------------------------------------------------------


def test_constructor_strips_trailing_slash():
    client = HttpClient("https://example.zendesk.com/", headers={})
    assert client.base_url == "https://example.zendesk.com"


def test_constructor_sets_default_and_custom_headers():
    client = HttpClient("https://example.zendesk.com", headers={"Authorization": "Bearer tok"})
    assert client.session.headers["Accept"] == "application/json"
    assert client.session.headers["Content-Type"] == "application/json"
    assert client.session.headers["Authorization"] == "Bearer tok"


def test_constructor_stores_timeout():
    client = HttpClient("https://example.zendesk.com", headers={}, timeout=60.0)
    assert client.timeout == 60.0


def test_constructor_default_timeout():
    client = HttpClient("https://example.zendesk.com", headers={})
    assert client.timeout == 30.0


def test_constructor_mounts_retry_adapter():
    client = HttpClient("https://example.zendesk.com", headers={})
    adapter = client.session.get_adapter("https://example.zendesk.com")
    assert isinstance(adapter, requests.adapters.HTTPAdapter)
    assert adapter.max_retries.total == 5
    assert adapter.max_retries.backoff_factor == 0.3
    assert 429 in adapter.max_retries.status_forcelist
    assert 500 in adapter.max_retries.status_forcelist


# ---------------------------------------------------------------------------
# _request: retry on connection errors
# ---------------------------------------------------------------------------


def test_request_retries_on_connection_error(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(200, json_data={"ok": True})

    original_session = client.session
    mocker.patch.object(original_session, "request", side_effect=requests.ConnectionError("Connection aborted"))
    mocker.patch.object(original_session, "close")

    new_session = Mock(spec=requests.Session)
    new_session.request.return_value = resp
    mocker.patch.object(client, "_new_session", return_value=new_session)

    result = client.get("/api/v2/tickets/1.json")

    original_session.close.assert_called_once()
    assert client.session is new_session
    new_session.request.assert_called_once_with(
        "GET", "https://example.zendesk.com/api/v2/tickets/1.json", params=None, timeout=30.0
    )
    assert result == {"ok": True}


def test_request_retries_on_remote_disconnected(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(200, json_data={"ok": True})

    original_session = client.session
    mocker.patch.object(
        original_session,
        "request",
        side_effect=RemoteDisconnected("Remote end closed connection without response"),
    )
    mocker.patch.object(original_session, "close")

    new_session = Mock(spec=requests.Session)
    new_session.request.return_value = resp
    mocker.patch.object(client, "_new_session", return_value=new_session)

    result = client.get("/api/v2/tickets/1.json")

    original_session.close.assert_called_once()
    assert client.session is new_session
    assert result == {"ok": True}


def test_request_does_not_retry_on_other_errors(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    mocker.patch.object(client.session, "request", side_effect=requests.Timeout("timed out"))

    with pytest.raises(requests.Timeout, match="timed out"):
        client.get("/api/v2/tickets/1.json")


def test_request_retry_failure_propagates(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})

    original_session = client.session
    mocker.patch.object(original_session, "request", side_effect=requests.ConnectionError("first"))
    mocker.patch.object(original_session, "close")

    new_session = Mock(spec=requests.Session)
    new_session.request.side_effect = requests.ConnectionError("second")
    mocker.patch.object(client, "_new_session", return_value=new_session)

    with pytest.raises(requests.ConnectionError, match="second"):
        client.get("/api/v2/tickets/1.json")


# ---------------------------------------------------------------------------
# GET raw
# ---------------------------------------------------------------------------


def test_get_raw_returns_json(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(200, json_data={"items": [1, 2, 3]})
    mocker.patch.object(client.session, "send", return_value=resp)

    url = "https://example.zendesk.com/api/v2/items?page[size]=10&page[after]=abc"
    result = client.get_raw(url)

    assert result == {"items": [1, 2, 3]}
    prepared = client.session.send.call_args[0][0]
    assert prepared.url == url


def test_get_raw_raises_on_error(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(404, text="Not Found")
    mocker.patch.object(client.session, "send", return_value=resp)

    with pytest.raises(NotFound, match="Not Found"):
        client.get_raw("https://example.zendesk.com/api/v2/items?page[size]=10")


def test_get_raw_retries_on_connection_error(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(200, json_data={"ok": True})

    original_session = client.session
    mocker.patch.object(original_session, "send", side_effect=requests.ConnectionError("Connection aborted"))
    mocker.patch.object(original_session, "close")

    new_session = Mock(spec=requests.Session)
    new_session.send.return_value = resp
    new_session.headers = original_session.headers
    mocker.patch.object(client, "_new_session", return_value=new_session)

    url = "https://example.zendesk.com/api/v2/items?page[size]=10"
    result = client.get_raw(url)

    original_session.close.assert_called_once()
    assert client.session is new_session
    prepared = new_session.send.call_args[0][0]
    assert prepared.url == url
    assert result == {"ok": True}


def test_get_raw_retries_on_remote_disconnected(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})
    resp = _make_response(200, json_data={"ok": True})

    original_session = client.session
    mocker.patch.object(
        original_session,
        "send",
        side_effect=RemoteDisconnected("Remote end closed connection without response"),
    )
    mocker.patch.object(original_session, "close")

    new_session = Mock(spec=requests.Session)
    new_session.send.return_value = resp
    new_session.headers = original_session.headers
    mocker.patch.object(client, "_new_session", return_value=new_session)

    result = client.get_raw("https://example.zendesk.com/api/v2/items?page[size]=10")

    original_session.close.assert_called_once()
    assert client.session is new_session
    assert result == {"ok": True}


def test_get_raw_retry_failure_propagates(mocker):
    client = HttpClient("https://example.zendesk.com", headers={})

    original_session = client.session
    mocker.patch.object(original_session, "send", side_effect=requests.ConnectionError("first"))
    mocker.patch.object(original_session, "close")

    new_session = Mock(spec=requests.Session)
    new_session.send.side_effect = requests.ConnectionError("second")
    new_session.headers = original_session.headers
    mocker.patch.object(client, "_new_session", return_value=new_session)

    with pytest.raises(requests.ConnectionError, match="second"):
        client.get_raw("https://example.zendesk.com/api/v2/items?page[size]=10")
