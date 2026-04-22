import pytest

from libzapi.application.commands.ticketing.organization_field_cmds import (
    CreateOrganizationFieldCmd,
    OrganizationFieldOptionCmd,
    UpdateOrganizationFieldCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import OrganizationFieldApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.organization_field_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


class TestFields:
    def test_list_all_yields(self, http, domain):
        http.get.return_value = {
            "organization_fields": [{"id": 1}, {"id": 2}],
            "meta": {"has_more": False},
            "links": {"next": None},
        }
        client = OrganizationFieldApiClient(http)
        items = list(client.list_all())
        assert len(items) == 2
        assert all(i["_cls"] == "OrganizationField" for i in items)
        http.get.assert_called_with("/api/v2/organization_fields")

    def test_get(self, http, domain):
        http.get.return_value = {"organization_field": {"id": 7}}
        client = OrganizationFieldApiClient(http)
        result = client.get(7)
        assert result["_cls"] == "OrganizationField"
        http.get.assert_called_with("/api/v2/organization_fields/7")

    def test_create(self, http, domain):
        http.post.return_value = {"organization_field": {"id": 1}}
        client = OrganizationFieldApiClient(http)
        client.create(
            CreateOrganizationFieldCmd(key="k", type="text", title="t")
        )
        http.post.assert_called_with(
            "/api/v2/organization_fields",
            {"organization_field": {"key": "k", "type": "text", "title": "t"}},
        )

    def test_update(self, http, domain):
        http.put.return_value = {"organization_field": {"id": 7}}
        client = OrganizationFieldApiClient(http)
        client.update(7, UpdateOrganizationFieldCmd(title="new"))
        http.put.assert_called_with(
            "/api/v2/organization_fields/7",
            {"organization_field": {"title": "new"}},
        )

    def test_delete(self, http):
        client = OrganizationFieldApiClient(http)
        client.delete(7)
        http.delete.assert_called_with("/api/v2/organization_fields/7")

    def test_reorder(self, http):
        client = OrganizationFieldApiClient(http)
        client.reorder([3, 1, 2])
        http.put.assert_called_with(
            "/api/v2/organization_fields/reorder",
            {"organization_field_ids": [3, 1, 2]},
        )


class TestOptions:
    def test_list_options(self, http, domain):
        http.get.return_value = {
            "custom_field_options": [{"id": 1}],
            "meta": {"has_more": False},
            "links": {"next": None},
        }
        client = OrganizationFieldApiClient(http)
        items = list(client.list_options(7))
        assert len(items) == 1
        assert items[0]["_cls"] == "OrganizationFieldOption"
        http.get.assert_called_with("/api/v2/organization_fields/7/options")

    def test_get_option(self, http, domain):
        http.get.return_value = {"custom_field_option": {"id": 9}}
        client = OrganizationFieldApiClient(http)
        result = client.get_option(7, 9)
        assert result["_cls"] == "OrganizationFieldOption"
        http.get.assert_called_with("/api/v2/organization_fields/7/options/9")

    def test_upsert_option(self, http, domain):
        http.post.return_value = {"custom_field_option": {"id": 9}}
        client = OrganizationFieldApiClient(http)
        client.upsert_option(7, OrganizationFieldOptionCmd(name="A", value="a"))
        http.post.assert_called_with(
            "/api/v2/organization_fields/7/options",
            {"custom_field_option": {"name": "A", "value": "a"}},
        )

    def test_delete_option(self, http):
        client = OrganizationFieldApiClient(http)
        client.delete_option(7, 9)
        http.delete.assert_called_with("/api/v2/organization_fields/7/options/9")


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = OrganizationFieldApiClient(http)
    with pytest.raises(error_cls):
        list(client.list_all())


def test_logical_key():
    from libzapi.domain.models.ticketing.organization_field import OrganizationField

    field = OrganizationField(
        id=1,
        url="u",
        type="text",
        key="Tier_Of_Account",
        title="t",
        description="d",
        raw_description="rd",
        position=0,
        active=True,
        system=False,
        regexp_for_validation=None,
        created_at=None,
        updated_at=None,
    )
    assert field.logical_key.as_str() == "organization_field:tier_of_account"
