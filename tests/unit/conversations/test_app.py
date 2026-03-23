import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.app import App
from libzapi.infrastructure.api_clients.conversations.app_api_client import AppApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.app_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(App, id=just("abc"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "app:abc"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.return_value = {"apps": [{}]}

    client = AppApiClient(https)
    list(client.list_all())

    https.get_raw.assert_called_with("https://example.zendesk.com/sc/v2/apps?page[size]=100")


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.return_value = {"app": {}}

    client = AppApiClient(https)
    client.get("app-1")

    https.get.assert_called_with("/v2/apps/app-1")


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"displayName": "My App"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {"app": {}}

    client = AppApiClient(https)
    client.create(mocker.Mock())

    https.post.assert_called_with("/v2/apps", {"displayName": "My App"})


# ── update ──────────────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"displayName": "Updated"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.patch.return_value = {"app": {}}

    client = AppApiClient(https)
    client.update("app-1", mocker.Mock())

    https.patch.assert_called_with("/v2/apps/app-1", {"displayName": "Updated"})


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = AppApiClient(https)
    client.delete("app-1")

    https.delete.assert_called_with("/v2/apps/app-1")


# ── error propagation: list_all (get) ──────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.side_effect = error_cls("error")

    client = AppApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all())


# ── error propagation: get ─────────────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.side_effect = error_cls("error")

    client = AppApiClient(https)

    with pytest.raises(error_cls):
        client.get("app-1")


# ── error propagation: create (post) ──────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_create_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_create", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = AppApiClient(https)

    with pytest.raises(error_cls):
        client.create(mocker.Mock())


# ── error propagation: delete ──────────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.delete.side_effect = error_cls("error")

    client = AppApiClient(https)

    with pytest.raises(error_cls):
        client.delete("app-1")
