import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.organization_cmds import (
    CreateOrganizationCmd,
    UpdateOrganizationCmd,
)
from libzapi.application.services.ticketing.organizations_service import (
    OrganizationsService,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_service(client=None):
    client = client or Mock()
    return OrganizationsService(client), client


# ---------------------------------------------------------------------------
# Delegation-only methods
# ---------------------------------------------------------------------------


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.orgs
        assert service.list_all() is sentinel.orgs
        client.list.assert_called_once_with()

    def test_list_by_user_delegates(self):
        service, client = _make_service()
        client.list_organizations.return_value = sentinel.orgs
        assert service.list_by_user(7) is sentinel.orgs
        client.list_organizations.assert_called_once_with(7)

    def test_count_delegates(self):
        service, client = _make_service()
        client.count.return_value = sentinel.count
        assert service.count() is sentinel.count

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.org
        assert service.get_by_id(99) is sentinel.org
        client.get.assert_called_once_with(99)

    def test_show_many_delegates(self):
        service, client = _make_service()
        client.show_many.return_value = sentinel.orgs
        result = service.show_many(organization_ids=[1, 2])
        client.show_many.assert_called_once_with(
            organization_ids=[1, 2], external_ids=None
        )
        assert result is sentinel.orgs

    def test_show_many_with_external_ids(self):
        service, client = _make_service()
        service.show_many(external_ids=["a", "b"])
        client.show_many.assert_called_once_with(
            organization_ids=None, external_ids=["a", "b"]
        )

    def test_search_delegates(self):
        service, client = _make_service()
        client.search.return_value = sentinel.matches
        assert service.search(name="Acme") is sentinel.matches
        client.search.assert_called_once_with(external_id=None, name="Acme")

    def test_autocomplete_delegates(self):
        service, client = _make_service()
        client.autocomplete.return_value = sentinel.matches
        assert service.autocomplete(name="Ac") is sentinel.matches
        client.autocomplete.assert_called_once_with(name="Ac")

    def test_list_related_delegates(self):
        service, client = _make_service()
        client.list_related.return_value = sentinel.related
        assert service.list_related(5) is sentinel.related
        client.list_related.assert_called_once_with(organization_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(organization_id=5)

    def test_destroy_many_delegates(self):
        service, client = _make_service()
        client.destroy_many.return_value = sentinel.job
        assert service.destroy_many([1, 2]) is sentinel.job
        client.destroy_many.assert_called_once_with(organization_ids=[1, 2])


# ---------------------------------------------------------------------------
# create / update / create_or_update
# ---------------------------------------------------------------------------


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.org

        result = service.create(name="Acme", notes="hi")

        client.create.assert_called_once()
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateOrganizationCmd)
        assert cmd.name == "Acme"
        assert cmd.notes == "hi"
        assert result is sentinel.org

    def test_passes_all_optional_fields(self):
        service, client = _make_service()
        service.create(
            name="Acme",
            domain_names=["a.com"],
            details="d",
            notes="n",
            group_id=1,
            shared_tickets=True,
            shared_comments=False,
            tags=["t"],
            organization_fields={"k": "v"},
            external_id="ext",
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.domain_names == ["a.com"]
        assert cmd.details == "d"
        assert cmd.notes == "n"
        assert cmd.group_id == 1
        assert cmd.shared_tickets is True
        assert cmd.shared_comments is False
        assert cmd.tags == ["t"]
        assert cmd.organization_fields == {"k": "v"}
        assert cmd.external_id == "ext"


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.org

        result = service.update(organization_id=42, notes="updated")

        client.update.assert_called_once()
        assert client.update.call_args.kwargs["organization_id"] == 42
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateOrganizationCmd)
        assert cmd.notes == "updated"
        assert result is sentinel.org

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(organization_id=1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.name is None
        assert cmd.notes is None


class TestCreateOrUpdate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create_or_update.return_value = sentinel.org

        result = service.create_or_update(name="Acme", external_id="ext-1")

        client.create_or_update.assert_called_once()
        cmd = client.create_or_update.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateOrganizationCmd)
        assert cmd.name == "Acme"
        assert cmd.external_id == "ext-1"
        assert result is sentinel.org


# ---------------------------------------------------------------------------
# create_many / update_many / update_many_individually
# ---------------------------------------------------------------------------


class TestCreateMany:
    def test_converts_dicts_to_create_cmds(self):
        service, client = _make_service()
        client.create_many.return_value = sentinel.job

        result = service.create_many(
            [{"name": "A"}, {"name": "B", "external_id": "ext"}]
        )

        entities = client.create_many.call_args.kwargs["entities"]
        assert len(entities) == 2
        assert all(isinstance(c, CreateOrganizationCmd) for c in entities)
        assert entities[0].name == "A"
        assert entities[1].name == "B"
        assert entities[1].external_id == "ext"
        assert result is sentinel.job

    def test_empty_input(self):
        service, client = _make_service()
        service.create_many([])
        assert client.create_many.call_args.kwargs["entities"] == []


class TestUpdateMany:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update_many.return_value = sentinel.job

        result = service.update_many([1, 2], tags=["vip"])

        assert client.update_many.call_args.kwargs["organization_ids"] == [1, 2]
        cmd = client.update_many.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateOrganizationCmd)
        assert cmd.tags == ["vip"]
        assert result is sentinel.job

    def test_no_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update_many([1])
        cmd = client.update_many.call_args.kwargs["entity"]
        assert cmd.name is None
        assert cmd.tags is None


class TestUpdateManyIndividually:
    def test_pairs_ids_with_update_cmds(self):
        service, client = _make_service()
        client.update_many_individually.return_value = sentinel.job

        result = service.update_many_individually(
            [(1, {"tags": ["a"]}), (2, {"notes": "b"})]
        )

        pairs = client.update_many_individually.call_args.kwargs["updates"]
        assert pairs[0][0] == 1
        assert isinstance(pairs[0][1], UpdateOrganizationCmd)
        assert pairs[0][1].tags == ["a"]
        assert pairs[1][0] == 2
        assert pairs[1][1].notes == "b"
        assert result is sentinel.job

    def test_empty_updates(self):
        service, client = _make_service()
        service.update_many_individually([])
        assert client.update_many_individually.call_args.kwargs["updates"] == []


# ---------------------------------------------------------------------------
# tag helpers
# ---------------------------------------------------------------------------


class TestTags:
    def test_list_tags_delegates(self):
        service, client = _make_service()
        client.list_tags.return_value = ["a", "b"]
        assert service.list_tags(5) == ["a", "b"]
        client.list_tags.assert_called_once_with(organization_id=5)

    def test_set_tags_delegates(self):
        service, client = _make_service()
        client.set_tags.return_value = ["a"]
        assert service.set_tags(5, ["a"]) == ["a"]
        client.set_tags.assert_called_once_with(organization_id=5, tags=["a"])

    def test_add_tags_delegates(self):
        service, client = _make_service()
        client.add_tags.return_value = ["a", "b"]
        assert service.add_tags(5, ["b"]) == ["a", "b"]
        client.add_tags.assert_called_once_with(organization_id=5, tags=["b"])

    def test_remove_tags_delegates(self):
        service, client = _make_service()
        client.remove_tags.return_value = ["a"]
        assert service.remove_tags(5, ["b"]) == ["a"]
        client.remove_tags.assert_called_once_with(organization_id=5, tags=["b"])


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(name="Acme")

    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_update_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.update.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.update(organization_id=1)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_all_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()
