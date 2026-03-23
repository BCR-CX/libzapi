import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.user import User
from libzapi.infrastructure.api_clients.conversations.user_api_client import UserApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.user_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(User, id=just("usr-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "sunco_user:usr-1"


# ── list_by_email ──────────────────────────────────────────────────────


def test_list_by_email_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.return_value = {"users": [{}]}

    client = UserApiClient(https)
    list(client.list_by_email("app-1", "test@example.com"))

    https.get_raw.assert_called_with(
        "https://example.zendesk.com/sc/v2/apps/app-1/users?filter[identities.email]=test@example.com&page[size]=100"
    )


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.return_value = {"user": {}}

    client = UserApiClient(https)
    client.get("app-1", "usr-1")

    https.get.assert_called_with("/v2/apps/app-1/users/usr-1")


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"externalId": "ext-1"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {"user": {}}

    client = UserApiClient(https)
    client.create("app-1", mocker.Mock())

    https.post.assert_called_with("/v2/apps/app-1/users", {"externalId": "ext-1"})


# ── update ──────────────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"profile": {"givenName": "John"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.patch.return_value = {"user": {}}

    client = UserApiClient(https)
    client.update("app-1", "usr-1", mocker.Mock())

    https.patch.assert_called_with("/v2/apps/app-1/users/usr-1", {"profile": {"givenName": "John"}})


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = UserApiClient(https)
    client.delete("app-1", "usr-1")

    https.delete.assert_called_with("/v2/apps/app-1/users/usr-1")


# ── delete_personal_info ────────────────────────────────────────────────


def test_delete_personal_info_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = UserApiClient(https)
    client.delete_personal_info("app-1", "usr-1")

    https.delete.assert_called_with("/v2/apps/app-1/users/usr-1/personalinformation")


# ── sync ────────────────────────────────────────────────────────────────


def test_sync_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {}

    client = UserApiClient(https)
    client.sync("app-1", "zd-123")

    https.post.assert_called_with("/v2/apps/app-1/users/zd-123/sync", {})


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
def test_list_by_email_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.side_effect = error_cls("error")

    client = UserApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_by_email("app-1", "test@example.com"))


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

    client = UserApiClient(https)

    with pytest.raises(error_cls):
        client.get("app-1", "usr-1")


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

    client = UserApiClient(https)

    with pytest.raises(error_cls):
        client.create("app-1", mocker.Mock())


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

    client = UserApiClient(https)

    with pytest.raises(error_cls):
        client.delete("app-1", "usr-1")
