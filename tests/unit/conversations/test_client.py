import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.client import Client
from libzapi.infrastructure.api_clients.conversations.client_api_client import ClientApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.client_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(Client, id=just("cli-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "sunco_client:cli-1"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.return_value = {"clients": [{}]}

    client = ClientApiClient(https)
    list(client.list_all("app-1", "usr-1"))

    https.get_raw.assert_called_with("https://example.zendesk.com/sc/v2/apps/app-1/users/usr-1/clients?page[size]=100")


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {"client": {}}

    client = ClientApiClient(https)
    client.create("app-1", "usr-1", {"platform": "web"})

    https.post.assert_called_with("/v2/apps/app-1/users/usr-1/clients", {"platform": "web"})


# ── remove ──────────────────────────────────────────────────────────────


def test_remove_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = ClientApiClient(https)
    client.remove("app-1", "usr-1", "cli-1")

    https.delete.assert_called_with("/v2/apps/app-1/users/usr-1/clients/cli-1")


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

    client = ClientApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("app-1", "usr-1"))


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
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = ClientApiClient(https)

    with pytest.raises(error_cls):
        client.create("app-1", "usr-1", {"platform": "web"})


# ── error propagation: remove (delete) ────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_remove_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.delete.side_effect = error_cls("error")

    client = ClientApiClient(https)

    with pytest.raises(error_cls):
        client.remove("app-1", "usr-1", "cli-1")
