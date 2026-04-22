import pytest

from libzapi.application.commands.ticketing.user_identity_cmds import (
    CreateUserIdentityCmd,
    UpdateUserIdentityCmd,
)
from libzapi.domain.errors import NotFound, Unauthorized
from libzapi.infrastructure.api_clients.ticketing import UserIdentityApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_identity_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_list_hits_expected_path(http, domain):
    http.get.return_value = {
        "identities": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = UserIdentityApiClient(http)
    items = list(client.list(42))
    http.get.assert_called_with("/api/v2/users/42/identities")
    assert len(items) == 2


# ---------------------------------------------------------------------------
# get / create / update / delete
# ---------------------------------------------------------------------------


def test_get_calls_endpoint(http, domain):
    http.get.return_value = {"identity": {"id": 9}}
    client = UserIdentityApiClient(http)
    client.get(user_id=3, identity_id=9)
    http.get.assert_called_with("/api/v2/users/3/identities/9")


def test_create_posts_payload(http, domain):
    http.post.return_value = {"identity": {"id": 1}}
    client = UserIdentityApiClient(http)
    client.create(
        user_id=3,
        entity=CreateUserIdentityCmd(
            type="email", value="x@y.com", verified=True, primary=False
        ),
    )
    http.post.assert_called_with(
        "/api/v2/users/3/identities",
        {
            "identity": {
                "type": "email",
                "value": "x@y.com",
                "verified": True,
                "primary": False,
            }
        },
    )


def test_update_puts_payload(http, domain):
    http.put.return_value = {"identity": {"id": 9}}
    client = UserIdentityApiClient(http)
    client.update(
        user_id=3,
        identity_id=9,
        entity=UpdateUserIdentityCmd(value="new@y.com"),
    )
    http.put.assert_called_with(
        "/api/v2/users/3/identities/9",
        {"identity": {"value": "new@y.com"}},
    )


def test_delete_calls_endpoint(http):
    client = UserIdentityApiClient(http)
    client.delete(user_id=3, identity_id=9)
    http.delete.assert_called_with("/api/v2/users/3/identities/9")


# ---------------------------------------------------------------------------
# make_primary / verify / request_verification
# ---------------------------------------------------------------------------


def test_make_primary_returns_list(http, domain):
    http.put.return_value = {"identities": [{"id": 1}, {"id": 2}]}
    client = UserIdentityApiClient(http)
    result = client.make_primary(user_id=3, identity_id=9)
    http.put.assert_called_with(
        "/api/v2/users/3/identities/9/make_primary", {}
    )
    assert len(result) == 2


def test_make_primary_handles_null(http, domain):
    http.put.return_value = {"identities": None}
    client = UserIdentityApiClient(http)
    assert client.make_primary(user_id=3, identity_id=9) == []


def test_verify_returns_identity(http, domain):
    http.put.return_value = {"identity": {"id": 9, "verified": True}}
    client = UserIdentityApiClient(http)
    result = client.verify(user_id=3, identity_id=9)
    http.put.assert_called_with("/api/v2/users/3/identities/9/verify", {})
    assert result["_cls"] == "UserIdentity"


def test_request_verification_puts_empty_body(http):
    client = UserIdentityApiClient(http)
    client.request_verification(user_id=3, identity_id=9)
    http.put.assert_called_with(
        "/api/v2/users/3/identities/9/request_verification", {}
    )


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_get_propagates_error(error_cls, http):
    http.get.side_effect = error_cls("boom")
    client = UserIdentityApiClient(http)
    with pytest.raises(error_cls):
        client.get(user_id=1, identity_id=2)


# ---------------------------------------------------------------------------
# Domain logical key
# ---------------------------------------------------------------------------


def test_user_identity_logical_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.user_identity import UserIdentity

    identity = UserIdentity(
        id=9,
        user_id=42,
        type="email",
        value="x@y.com",
        verified=True,
        primary=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert identity.logical_key.as_str() == "user_identity:u42_id9"
