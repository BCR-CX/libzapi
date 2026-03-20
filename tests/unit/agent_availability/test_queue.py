import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.agent_availability.queue_api_client import QueueApiClient


MODULE = "libzapi.infrastructure.api_clients.agent_availability.queue_api_client"
BASE = "/api/v2/queues"


# ── list ────────────────────────────────────────────────────────────────


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"queues": [{"id": "q-1", "name": "Default"}]}

    client = QueueApiClient(https)
    list(client.list())

    https.get.assert_called_with(BASE)


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"queue": {"id": "q-1"}}

    client = QueueApiClient(https)
    client.get("q-1")

    https.get.assert_called_with(f"{BASE}/q-1")


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"queue": {"name": "Test"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"queue": {"id": "q-1", "name": "Test"}}

    client = QueueApiClient(https)
    client.create(mocker.Mock())

    https.post.assert_called_with(BASE, {"queue": {"name": "Test"}})


# ── update ──────────────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"queue": {"name": "Updated"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"queue": {"id": "q-1", "name": "Updated"}}

    client = QueueApiClient(https)
    client.update("q-1", mocker.Mock())

    https.put.assert_called_with(f"{BASE}/q-1", {"queue": {"name": "Updated"}})


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = QueueApiClient(https)
    client.delete("q-1")

    https.delete.assert_called_with(f"{BASE}/q-1")


# ── list_definitions ───────────────────────────────────────────────────


def test_list_definitions_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"definitions": []}

    client = QueueApiClient(https)
    client.list_definitions()

    https.get.assert_called_with(f"{BASE}/definitions")


# ── reorder ─────────────────────────────────────────────────────────────


def test_reorder_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {}

    client = QueueApiClient(https)
    client.reorder(["q-2", "q-1"])

    https.patch.assert_called_with(f"{BASE}/order", {"queue_ids": ["q-2", "q-1"]})


# ── error propagation ──────────────────────────────────────────────────


ERROR_CLASSES = [
    pytest.param(Unauthorized, id="401"),
    pytest.param(NotFound, id="404"),
    pytest.param(UnprocessableEntity, id="422"),
    pytest.param(RateLimited, id="429"),
]


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_list_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = QueueApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = QueueApiClient(https)

    with pytest.raises(error_cls):
        client.get("q-1")


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_create_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"queue": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.side_effect = error_cls("error")

    client = QueueApiClient(https)

    with pytest.raises(error_cls):
        client.create(mocker.Mock())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_update_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"queue": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.side_effect = error_cls("error")

    client = QueueApiClient(https)

    with pytest.raises(error_cls):
        client.update("q-1", mocker.Mock())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.delete.side_effect = error_cls("error")

    client = QueueApiClient(https)

    with pytest.raises(error_cls):
        client.delete("q-1")
