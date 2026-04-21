import pytest

from libzapi.application.commands.ticketing.organization_cmds import (
    CreateOrganizationCmd,
    UpdateOrganizationCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import OrganizationApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.organization_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list", [], "/api/v2/organizations", "organizations"),
        ("list_organizations", [456], "/api/v2/users/456/organizations", "organizations"),
    ],
)
def test_organization_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = OrganizationApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_organization_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"organization": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.organization_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = OrganizationApiClient(https)
    client.get(99)

    https.get.assert_called_with("/api/v2/organizations/99")


def test_organization_api_client_search_by_external_id(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"organizations": []}

    client = OrganizationApiClient(https)
    list(client.search(external_id="ext_123"))

    https.get.assert_called_with("/api/v2/organizations/search?external_id=ext_123")


def test_organization_api_client_search_by_name(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"organizations": []}

    client = OrganizationApiClient(https)
    list(client.search(name="Acme"))

    https.get.assert_called_with("/api/v2/organizations/search?name=Acme")


def test_organization_api_client_search_raises_without_params():
    client = OrganizationApiClient(None)

    with pytest.raises(ValueError, match="Either external_id or name must be provided"):
        list(client.search())


def test_organization_api_client_count(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"count": {"refreshed_at": "2024-01-01T00:00:00Z", "value": 42}}

    client = OrganizationApiClient(https)
    result = client.count()

    https.get.assert_called_with("/api/v2/organizations/count")
    assert result.value == 42


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_organization_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = OrganizationApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


# ---------------------------------------------------------------------------
# Iterator bodies
# ---------------------------------------------------------------------------


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "organizations": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = OrganizationApiClient(http)
    result = list(client.list())
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_list_organizations_yields_items(http, domain):
    http.get.return_value = {
        "organizations": [{"id": 1}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = OrganizationApiClient(http)
    result = list(client.list_organizations(123))
    assert len(result) == 1


def test_autocomplete_yields_items(http, domain):
    http.get.return_value = {"organizations": [{"id": 1}, {"id": 2}]}
    client = OrganizationApiClient(http)
    result = list(client.autocomplete(name="Ac"))
    assert len(result) == 2
    http.get.assert_called_with("/api/v2/organizations/autocomplete?name=Ac")


def test_search_handles_null_organizations_key(http, domain):
    http.get.return_value = {"organizations": None}
    client = OrganizationApiClient(http)
    assert list(client.search(name="missing")) == []


def test_search_yields_items_when_results_present(http, domain):
    http.get.return_value = {"organizations": [{"id": 1}, {"id": 2}]}
    client = OrganizationApiClient(http)
    result = list(client.search(name="Acme"))
    assert len(result) == 2


def test_organization_logical_key_normalises_name():
    from libzapi.domain.models.ticketing.organization import Organization
    from datetime import datetime

    org = Organization(
        id=1,
        url="https://x",
        name="Acme Corp",
        shared_tickets=False,
        shared_comments=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        domain_names=[],
        details=None,
        notes=None,
        tags=[],
        organization_fields={},
    )
    assert org.logical_key.as_str() == "organization:acme_corp"


# ---------------------------------------------------------------------------
# show_many
# ---------------------------------------------------------------------------


def test_show_many_by_ids(http, domain):
    http.get.return_value = {"organizations": [{"id": 1}, {"id": 2}]}
    client = OrganizationApiClient(http)
    result = list(client.show_many(organization_ids=[1, 2]))
    http.get.assert_called_with("/api/v2/organizations/show_many?ids=1,2")
    assert len(result) == 2


def test_show_many_by_external_ids(http, domain):
    http.get.return_value = {"organizations": []}
    client = OrganizationApiClient(http)
    list(client.show_many(external_ids=["a", "b"]))
    http.get.assert_called_with(
        "/api/v2/organizations/show_many?external_ids=a,b"
    )


def test_show_many_raises_without_params(http):
    client = OrganizationApiClient(http)
    with pytest.raises(ValueError, match="Either organization_ids or external_ids"):
        list(client.show_many())


# ---------------------------------------------------------------------------
# list_related
# ---------------------------------------------------------------------------


def test_list_related_uses_related_endpoint(http, domain):
    http.get.return_value = {
        "organization_related": {"tickets_count": 3, "users_count": 5}
    }
    client = OrganizationApiClient(http)
    result = client.list_related(organization_id=99)
    http.get.assert_called_with("/api/v2/organizations/99/related")
    assert result["tickets_count"] == 3


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"organization": {"id": 1, "name": "Acme"}}
    client = OrganizationApiClient(http)
    result = client.create(CreateOrganizationCmd(name="Acme"))
    http.post.assert_called_with(
        "/api/v2/organizations", {"organization": {"name": "Acme"}}
    )
    assert result["name"] == "Acme"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"organization": {"id": 1, "notes": "hi"}}
    client = OrganizationApiClient(http)
    client.update(organization_id=1, entity=UpdateOrganizationCmd(notes="hi"))
    http.put.assert_called_with(
        "/api/v2/organizations/1", {"organization": {"notes": "hi"}}
    )


def test_delete_calls_delete(http):
    client = OrganizationApiClient(http)
    client.delete(organization_id=7)
    http.delete.assert_called_with("/api/v2/organizations/7")


# ---------------------------------------------------------------------------
# Bulk operations
# ---------------------------------------------------------------------------


def test_create_many_posts_list(http, domain):
    http.post.return_value = {"job_status": {"id": "abc"}}
    client = OrganizationApiClient(http)
    client.create_many(
        [CreateOrganizationCmd(name="A"), CreateOrganizationCmd(name="B")]
    )
    http.post.assert_called_with(
        "/api/v2/organizations/create_many",
        {"organizations": [{"name": "A"}, {"name": "B"}]},
    )


def test_create_or_update_posts_payload(http, domain):
    http.post.return_value = {"organization": {"id": 1}}
    client = OrganizationApiClient(http)
    client.create_or_update(CreateOrganizationCmd(name="Acme", external_id="e"))
    http.post.assert_called_with(
        "/api/v2/organizations/create_or_update",
        {"organization": {"name": "Acme", "external_id": "e"}},
    )


def test_update_many_puts_with_ids(http, domain):
    http.put.return_value = {"job_status": {"id": "abc"}}
    client = OrganizationApiClient(http)
    client.update_many([1, 2], UpdateOrganizationCmd(notes="n"))
    http.put.assert_called_with(
        "/api/v2/organizations/update_many?ids=1,2",
        {"organization": {"notes": "n"}},
    )


def test_update_many_individually_puts_bodies(http, domain):
    http.put.return_value = {"job_status": {"id": "abc"}}
    client = OrganizationApiClient(http)
    client.update_many_individually(
        [
            (1, UpdateOrganizationCmd(tags=["a"])),
            (2, UpdateOrganizationCmd(notes="n")),
        ]
    )
    http.put.assert_called_with(
        "/api/v2/organizations/update_many",
        {
            "organizations": [
                {"tags": ["a"], "id": 1},
                {"notes": "n", "id": 2},
            ]
        },
    )


def test_destroy_many_deletes_with_ids(http, domain):
    http.delete.return_value = {"job_status": {"id": "abc"}}
    client = OrganizationApiClient(http)
    client.destroy_many([1, 2])
    http.delete.assert_called_with("/api/v2/organizations/destroy_many?ids=1,2")


def test_destroy_many_handles_none_response(http, domain):
    http.delete.return_value = None
    client = OrganizationApiClient(http)
    with pytest.raises(KeyError):
        client.destroy_many([1])


# ---------------------------------------------------------------------------
# tag helpers
# ---------------------------------------------------------------------------


def test_list_tags_returns_list(http):
    http.get.return_value = {"tags": ["a", "b"]}
    client = OrganizationApiClient(http)
    assert client.list_tags(organization_id=1) == ["a", "b"]
    http.get.assert_called_with("/api/v2/organizations/1/tags")


def test_list_tags_missing_key_returns_empty(http):
    http.get.return_value = {}
    client = OrganizationApiClient(http)
    assert client.list_tags(organization_id=1) == []


def test_set_tags_posts_tags(http):
    http.post.return_value = {"tags": ["a"]}
    client = OrganizationApiClient(http)
    assert client.set_tags(organization_id=1, tags=["a"]) == ["a"]
    http.post.assert_called_with("/api/v2/organizations/1/tags", {"tags": ["a"]})


def test_add_tags_puts_tags(http):
    http.put.return_value = {"tags": ["a", "b"]}
    client = OrganizationApiClient(http)
    assert client.add_tags(organization_id=1, tags=["b"]) == ["a", "b"]
    http.put.assert_called_with("/api/v2/organizations/1/tags", {"tags": ["b"]})


def test_remove_tags_deletes_with_json(http):
    http.delete.return_value = {"tags": ["a"]}
    client = OrganizationApiClient(http)
    assert client.remove_tags(organization_id=1, tags=["b"]) == ["a"]
    http.delete.assert_called_with(
        "/api/v2/organizations/1/tags", json={"tags": ["b"]}
    )


def test_remove_tags_handles_none_response(http):
    http.delete.return_value = None
    client = OrganizationApiClient(http)
    assert client.remove_tags(organization_id=1, tags=["b"]) == []
