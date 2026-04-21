import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.user_cmds import CreateUserCmd, UpdateUserCmd
from libzapi.application.services.ticketing.users_service import UsersService
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return UsersService(client), client


# ---------------------------------------------------------------------------
# simple delegation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method",
    ["list_all", "count", "me", "me_settings", "list_deleted", "count_deleted"],
)
def test_no_arg_delegation(method):
    service, client = _make_service()
    getattr(client, method).return_value = sentinel.result

    result = getattr(service, method)()

    getattr(client, method).assert_called_once_with()
    assert result is sentinel.result


@pytest.mark.parametrize(
    "method, arg",
    [
        ("list_by_group", 11),
        ("list_by_organization", 22),
        ("count_by_group", 11),
        ("count_by_organization", 22),
    ],
)
def test_positional_id_delegation(method, arg):
    service, client = _make_service()
    getattr(client, method).return_value = sentinel.result

    result = getattr(service, method)(arg)

    getattr(client, method).assert_called_once_with(arg)
    assert result is sentinel.result


def test_get_by_id_delegates_to_get():
    service, client = _make_service()
    client.get.return_value = sentinel.user

    assert service.get_by_id(5) is sentinel.user
    client.get.assert_called_once_with(5)


def test_show_many_delegates():
    service, client = _make_service()
    client.show_many.return_value = sentinel.users

    assert service.show_many([1, 2]) is sentinel.users
    client.show_many.assert_called_once_with(user_ids=[1, 2])


def test_search_passes_kwargs():
    service, client = _make_service()
    service.search(query="q", external_id="ext")
    client.search.assert_called_once_with(query="q", external_id="ext")


def test_autocomplete_passes_name():
    service, client = _make_service()
    service.autocomplete(name="al")
    client.autocomplete.assert_called_once_with(name="al")


def test_list_related_passes_user_id():
    service, client = _make_service()
    service.list_related(user_id=5)
    client.list_related.assert_called_once_with(user_id=5)


def test_list_compliance_passes_user_id():
    service, client = _make_service()
    service.list_compliance_deletion_statuses(user_id=5)
    client.list_compliance_deletion_statuses.assert_called_once_with(user_id=5)


def test_show_deleted_passes_id():
    service, client = _make_service()
    service.show_deleted(deleted_user_id=11)
    client.show_deleted.assert_called_once_with(deleted_user_id=11)


def test_update_me_settings_passes_dict():
    service, client = _make_service()
    service.update_me_settings({"k": "v"})
    client.update_me_settings.assert_called_once_with(settings={"k": "v"})


def test_list_entitlements_passes_user_id():
    service, client = _make_service()
    service.list_entitlements(user_id=5)
    client.list_entitlements.assert_called_once_with(user_id=5)


def test_merge_passes_source_target():
    service, client = _make_service()
    service.merge(source_user_id=1, target_user_id=2)
    client.merge.assert_called_once_with(source_user_id=1, target_user_id=2)


def test_permanently_delete_passes_id():
    service, client = _make_service()
    service.permanently_delete(deleted_user_id=11)
    client.permanently_delete.assert_called_once_with(deleted_user_id=11)


def test_logout_many_passes_ids():
    service, client = _make_service()
    service.logout_many([1, 2])
    client.logout_many.assert_called_once_with(user_ids=[1, 2])


# ---------------------------------------------------------------------------
# cmd-building methods
# ---------------------------------------------------------------------------


class TestCreate:
    def test_builds_create_user_cmd(self):
        service, client = _make_service()
        client.create.return_value = sentinel.user

        result = service.create(name="n", email="e@x.y", role="end-user", tags=["a"])

        entity = client.create.call_args.kwargs["entity"]
        assert isinstance(entity, CreateUserCmd)
        assert entity.name == "n"
        assert entity.email == "e@x.y"
        assert entity.role == "end-user"
        assert entity.tags == ["a"]
        assert result is sentinel.user

    def test_requires_name(self):
        service, _ = _make_service()
        with pytest.raises(TypeError):
            service.create(email="e@x.y")


class TestUpdate:
    def test_builds_update_user_cmd(self):
        service, client = _make_service()
        client.update.return_value = sentinel.user

        result = service.update(user_id=5, name="new")

        assert client.update.call_args.kwargs["user_id"] == 5
        entity = client.update.call_args.kwargs["entity"]
        assert isinstance(entity, UpdateUserCmd)
        assert entity.name == "new"
        assert result is sentinel.user

    def test_update_with_no_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(user_id=5)
        entity = client.update.call_args.kwargs["entity"]
        assert entity.name is None


def test_delete_delegates():
    service, client = _make_service()
    client.delete.return_value = sentinel.user

    assert service.delete(5) is sentinel.user
    client.delete.assert_called_once_with(user_id=5)


class TestCreateMany:
    def test_converts_list_of_dicts(self):
        service, client = _make_service()
        client.create_many.return_value = sentinel.job

        result = service.create_many(
            [{"name": "a", "email": "a@x.y"}, {"name": "b"}]
        )

        entities = client.create_many.call_args.kwargs["entities"]
        assert len(entities) == 2
        assert all(isinstance(e, CreateUserCmd) for e in entities)
        assert entities[0].name == "a"
        assert entities[0].email == "a@x.y"
        assert entities[1].name == "b"
        assert result is sentinel.job


def test_create_or_update_builds_cmd():
    service, client = _make_service()
    service.create_or_update(name="n", email="e@x.y")
    entity = client.create_or_update.call_args.kwargs["entity"]
    assert isinstance(entity, CreateUserCmd)
    assert entity.name == "n"


def test_create_or_update_many_builds_list():
    service, client = _make_service()
    service.create_or_update_many([{"name": "a"}])
    entities = client.create_or_update_many.call_args.kwargs["entities"]
    assert len(entities) == 1
    assert entities[0].name == "a"


class TestUpdateMany:
    def test_update_many_builds_update_cmd(self):
        service, client = _make_service()
        client.update_many.return_value = sentinel.job

        service.update_many([1, 2], tags=["a"])

        assert client.update_many.call_args.kwargs["user_ids"] == [1, 2]
        entity = client.update_many.call_args.kwargs["entity"]
        assert isinstance(entity, UpdateUserCmd)
        assert entity.tags == ["a"]

    def test_update_many_individually_builds_pairs(self):
        service, client = _make_service()
        client.update_many_individually.return_value = sentinel.job

        service.update_many_individually(
            [(1, {"tags": ["x"]}), (2, {"role": "agent"})]
        )

        pairs = client.update_many_individually.call_args.kwargs["updates"]
        assert pairs[0][0] == 1
        assert isinstance(pairs[0][1], UpdateUserCmd)
        assert pairs[0][1].tags == ["x"]
        assert pairs[1][1].role == "agent"


def test_destroy_many_delegates():
    service, client = _make_service()
    service.destroy_many([1, 2])
    client.destroy_many.assert_called_once_with(user_ids=[1, 2])


def test_request_create_builds_cmd():
    service, client = _make_service()
    client.request_create.return_value = {"ok": True}

    assert service.request_create(name="n", email="e@x.y") == {"ok": True}
    entity = client.request_create.call_args.kwargs["entity"]
    assert isinstance(entity, CreateUserCmd)
    assert entity.name == "n"


# ---------------------------------------------------------------------------
# tag helpers
# ---------------------------------------------------------------------------


def test_list_tags_delegates():
    service, client = _make_service()
    client.list_tags.return_value = ["a"]
    assert service.list_tags(5) == ["a"]
    client.list_tags.assert_called_once_with(user_id=5)


def test_set_tags_delegates():
    service, client = _make_service()
    client.set_tags.return_value = ["a"]
    assert service.set_tags(5, ["a"]) == ["a"]
    client.set_tags.assert_called_once_with(user_id=5, tags=["a"])


def test_add_tags_delegates():
    service, client = _make_service()
    client.add_tags.return_value = ["a", "b"]
    assert service.add_tags(5, ["b"]) == ["a", "b"]
    client.add_tags.assert_called_once_with(user_id=5, tags=["b"])


def test_remove_tags_delegates():
    service, client = _make_service()
    client.remove_tags.return_value = ["a"]
    assert service.remove_tags(5, ["b"]) == ["a"]
    client.remove_tags.assert_called_once_with(user_id=5, tags=["b"])


# ---------------------------------------------------------------------------
# error propagation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_create_propagates_error(error_cls):
    service, client = _make_service()
    client.create.side_effect = error_cls("boom")

    with pytest.raises(error_cls):
        service.create(name="n")


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_list_all_propagates_error(error_cls):
    service, client = _make_service()
    client.list_all.side_effect = error_cls("boom")

    with pytest.raises(error_cls):
        service.list_all()
