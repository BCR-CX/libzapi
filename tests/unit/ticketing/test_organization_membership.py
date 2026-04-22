import pytest

from libzapi.application.commands.ticketing.organization_membership_cmds import (
    CreateOrganizationMembershipCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import (
    OrganizationMembershipApiClient,
)


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.organization_membership_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# Iterators
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method, args, path",
    [
        ("list", [], "/api/v2/organization_memberships"),
        (
            "list_by_user",
            [42],
            "/api/v2/users/42/organization_memberships",
        ),
        (
            "list_by_organization",
            [7],
            "/api/v2/organizations/7/organization_memberships",
        ),
    ],
)
def test_list_endpoints_hit_expected_path(method, args, path, http, domain):
    http.get.return_value = {"organization_memberships": []}
    client = OrganizationMembershipApiClient(http)
    list(getattr(client, method)(*args))
    http.get.assert_called_with(path)


@pytest.mark.parametrize(
    "method, args",
    [
        ("list", ()),
        ("list_by_user", (42,)),
        ("list_by_organization", (7,)),
    ],
)
def test_list_yields_items(method, args, http, domain):
    http.get.return_value = {
        "organization_memberships": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = OrganizationMembershipApiClient(http)
    assert len(list(getattr(client, method)(*args))) == 2


# ---------------------------------------------------------------------------
# get / get_for_user
# ---------------------------------------------------------------------------


def test_get_calls_endpoint(http, domain):
    http.get.return_value = {"organization_membership": {"id": 5}}
    client = OrganizationMembershipApiClient(http)
    client.get(membership_id=5)
    http.get.assert_called_with("/api/v2/organization_memberships/5")


def test_get_for_user_calls_endpoint(http, domain):
    http.get.return_value = {"organization_membership": {"id": 5}}
    client = OrganizationMembershipApiClient(http)
    client.get_for_user(user_id=3, membership_id=5)
    http.get.assert_called_with(
        "/api/v2/users/3/organization_memberships/5"
    )


# ---------------------------------------------------------------------------
# create / create_for_user
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"organization_membership": {"id": 1}}
    client = OrganizationMembershipApiClient(http)
    client.create(CreateOrganizationMembershipCmd(user_id=3, organization_id=4))
    http.post.assert_called_with(
        "/api/v2/organization_memberships",
        {"organization_membership": {"user_id": 3, "organization_id": 4}},
    )


def test_create_for_user_posts_payload(http, domain):
    http.post.return_value = {"organization_membership": {"id": 1}}
    client = OrganizationMembershipApiClient(http)
    client.create_for_user(
        user_id=3,
        entity=CreateOrganizationMembershipCmd(
            user_id=3, organization_id=4, default=True
        ),
    )
    http.post.assert_called_with(
        "/api/v2/users/3/organization_memberships",
        {
            "organization_membership": {
                "user_id": 3,
                "organization_id": 4,
                "default": True,
            }
        },
    )


# ---------------------------------------------------------------------------
# delete variants
# ---------------------------------------------------------------------------


def test_delete_calls_endpoint(http):
    client = OrganizationMembershipApiClient(http)
    client.delete(membership_id=9)
    http.delete.assert_called_with("/api/v2/organization_memberships/9")


def test_delete_for_user_calls_endpoint(http):
    client = OrganizationMembershipApiClient(http)
    client.delete_for_user(user_id=3, membership_id=9)
    http.delete.assert_called_with(
        "/api/v2/users/3/organization_memberships/9"
    )


# ---------------------------------------------------------------------------
# make_default
# ---------------------------------------------------------------------------


def test_make_default_puts_and_parses_results(http, domain):
    http.put.return_value = {"results": [{"id": 1}, {"id": 2}]}
    client = OrganizationMembershipApiClient(http)
    result = client.make_default(user_id=3, membership_id=9)
    http.put.assert_called_with(
        "/api/v2/users/3/organization_memberships/9/make_default", {}
    )
    assert len(result) == 2


def test_make_default_with_null_results(http, domain):
    http.put.return_value = {"results": None}
    client = OrganizationMembershipApiClient(http)
    assert client.make_default(user_id=3, membership_id=9) == []


# ---------------------------------------------------------------------------
# bulk
# ---------------------------------------------------------------------------


def test_create_many_posts_list(http, domain):
    http.post.return_value = {"job_status": {"id": "abc"}}
    client = OrganizationMembershipApiClient(http)
    client.create_many(
        [
            CreateOrganizationMembershipCmd(user_id=1, organization_id=2),
            CreateOrganizationMembershipCmd(
                user_id=3, organization_id=4, default=True
            ),
        ]
    )
    http.post.assert_called_with(
        "/api/v2/organization_memberships/create_many",
        {
            "organization_memberships": [
                {"user_id": 1, "organization_id": 2},
                {"user_id": 3, "organization_id": 4, "default": True},
            ]
        },
    )


def test_destroy_many_builds_path(http, domain):
    http.delete.return_value = {"job_status": {"id": "abc"}}
    client = OrganizationMembershipApiClient(http)
    client.destroy_many([1, 2, 3])
    http.delete.assert_called_with(
        "/api/v2/organization_memberships/destroy_many?ids=1,2,3"
    )


def test_destroy_many_handles_none_response(http, domain):
    http.delete.return_value = None
    client = OrganizationMembershipApiClient(http)
    with pytest.raises(KeyError):
        client.destroy_many([1])


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = OrganizationMembershipApiClient(http)
    with pytest.raises(error_cls):
        list(client.list())


# ---------------------------------------------------------------------------
# Domain logical key
# ---------------------------------------------------------------------------


def test_organization_membership_logical_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.organization_membership import (
        OrganizationMembership,
    )

    om = OrganizationMembership(
        id=1,
        user_id=42,
        organization_id=7,
        default=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert om.logical_key.as_str() == "organization_membership:u42_o7"
