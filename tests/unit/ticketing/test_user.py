import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.application.commands.ticketing.user_cmds import CreateUserCmd, UpdateUserCmd
from libzapi.domain.models.ticketing.user import User
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import UserApiClient

strategy = builds(
    User,
    id=just(123),
)


@given(strategy)
def test_logical_key_from_id(obj: User):
    assert obj.logical_key.as_str() == "user:id_123"


def test_user_api_client_get_one(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"user": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_api_client.to_domain",
        return_value=mocker.Mock(),  # does not matter what it is
    )

    client = UserApiClient(https)

    client.get(fake_id)

    https.get.assert_called_with(f"/api/v2/users/{fake_id}")


@pytest.mark.parametrize(
    "method_name, resource_type, filter_value, path",
    [
        ("list_all", None, None, "/api/v2/users"),
        ("list_by_group", "group_id", 123, "/api/v2/groups/123/users"),
        ("list_by_organization", "organization_id", 145, "/api/v2/organizations/145/users"),
    ],
)
def test_suspended_ticket_api_client_list_all(mocker, method_name, resource_type, filter_value, path):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"users": []}

    client = UserApiClient(https)

    method = getattr(client, method_name, None)
    if filter_value is not None:
        list(method(filter_value))
    else:
        list(method())

    https.get.assert_called_with(path)


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_user_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = UserApiClient(https)

    with pytest.raises(error_cls):
        client.get(1)


# ---------------------------------------------------------------------------
# read endpoints
# ---------------------------------------------------------------------------


@pytest.fixture
def http(mocker):
    stub = mocker.Mock()
    stub.base_url = "https://example.zendesk.com"
    return stub


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_api_client.to_domain",
        return_value=mocker.Mock(),
    )


def test_me_gets_users_me(http, domain):
    http.get.return_value = {"user": {}}
    client = UserApiClient(http)

    client.me()

    http.get.assert_called_once_with("/api/v2/users/me")


def test_show_many_joins_ids(http, domain):
    http.get.return_value = {"users": [{}, {}]}
    client = UserApiClient(http)

    list(client.show_many(user_ids=[1, 2, 3]))

    http.get.assert_called_once_with("/api/v2/users/show_many?ids=1,2,3")


def test_search_by_external_id(http, domain):
    http.get.return_value = {"users": []}
    client = UserApiClient(http)

    list(client.search(external_id="ext-1"))

    http.get.assert_called_with("/api/v2/users/search?external_id=ext-1")


def test_search_by_query(http, domain):
    http.get.return_value = {"users": []}
    client = UserApiClient(http)

    list(client.search(query="alice"))

    http.get.assert_called_with("/api/v2/users/search?query=alice")


def test_search_with_no_args_uses_empty_query(http, domain):
    http.get.return_value = {"users": []}
    client = UserApiClient(http)

    list(client.search())

    http.get.assert_called_with("/api/v2/users/search?query=")


def test_autocomplete_posts_name(http, domain):
    http.post.return_value = {"users": [{}]}
    client = UserApiClient(http)

    list(client.autocomplete(name="al"))

    http.post.assert_called_once_with("/api/v2/users/autocomplete", {"name": "al"})


def test_autocomplete_missing_users_key(http, domain):
    http.post.return_value = {}
    client = UserApiClient(http)

    assert list(client.autocomplete(name="al")) == []


def test_list_related(http, domain):
    http.get.return_value = {"user_related": {"requested_tickets": 2}}
    client = UserApiClient(http)

    client.list_related(user_id=5)

    http.get.assert_called_once_with("/api/v2/users/5/related")


def test_list_compliance_deletion_statuses(http, domain):
    http.get.return_value = {"compliance_deletion_statuses": [{}]}
    client = UserApiClient(http)

    list(client.list_compliance_deletion_statuses(user_id=5))

    http.get.assert_called_once_with("/api/v2/users/5/compliance_deletion_statuses")


def test_list_compliance_missing_key_returns_empty(http, domain):
    http.get.return_value = {}
    client = UserApiClient(http)

    assert list(client.list_compliance_deletion_statuses(user_id=5)) == []


@pytest.mark.parametrize(
    "method, path",
    [
        ("count", "/api/v2/users/count"),
    ],
)
def test_count_methods(method, path, http, domain):
    http.get.return_value = {"count": {}}
    mocker_patch = http  # keep name simple
    client = UserApiClient(http)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "libzapi.infrastructure.api_clients.ticketing.user_api_client.to_count_snapshot",
            lambda data: data,
        )
        getattr(client, method)()
    mocker_patch.get.assert_called_with(path)


def test_count_by_group(http, mocker):
    http.get.return_value = {"count": {"value": 1}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_api_client.to_count_snapshot",
        return_value="snapshot",
    )
    client = UserApiClient(http)

    assert client.count_by_group(group_id=11) == "snapshot"
    http.get.assert_called_once_with("/api/v2/groups/11/users/count")


def test_count_by_organization(http, mocker):
    http.get.return_value = {"count": {"value": 2}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_api_client.to_count_snapshot",
        return_value="snapshot",
    )
    client = UserApiClient(http)

    assert client.count_by_organization(organization_id=22) == "snapshot"
    http.get.assert_called_once_with("/api/v2/organizations/22/users/count")


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_mapped_payload(http, domain):
    http.post.return_value = {"user": {}}
    client = UserApiClient(http)

    client.create(entity=CreateUserCmd(name="n", email="e@x.y"))

    path, payload = http.post.call_args.args
    assert path == "/api/v2/users"
    assert payload == {"user": {"name": "n", "email": "e@x.y"}}


def test_update_puts_mapped_payload(http, domain):
    http.put.return_value = {"user": {}}
    client = UserApiClient(http)

    client.update(user_id=42, entity=UpdateUserCmd(name="new"))

    path, payload = http.put.call_args.args
    assert path == "/api/v2/users/42"
    assert payload == {"user": {"name": "new"}}


def test_delete_returns_domain(http, domain):
    http.delete.return_value = {"user": {}}
    client = UserApiClient(http)

    client.delete(user_id=42)

    http.delete.assert_called_once_with("/api/v2/users/42")


def test_delete_handles_empty_response(http, domain):
    http.delete.return_value = None
    client = UserApiClient(http)

    with pytest.raises(KeyError):
        client.delete(user_id=42)


# ---------------------------------------------------------------------------
# bulk operations
# ---------------------------------------------------------------------------


def test_create_many_posts_list_body(http, domain):
    http.post.return_value = {"job_status": {}}
    client = UserApiClient(http)

    client.create_many(entities=[CreateUserCmd(name="a"), CreateUserCmd(name="b")])

    path, payload = http.post.call_args.args
    assert path == "/api/v2/users/create_many"
    assert payload == {"users": [{"name": "a"}, {"name": "b"}]}


def test_create_or_update(http, domain):
    http.post.return_value = {"user": {}}
    client = UserApiClient(http)

    client.create_or_update(entity=CreateUserCmd(name="n", email="e@x.y"))

    http.post.assert_called_once_with(
        "/api/v2/users/create_or_update", {"user": {"name": "n", "email": "e@x.y"}}
    )


def test_create_or_update_many(http, domain):
    http.post.return_value = {"job_status": {}}
    client = UserApiClient(http)

    client.create_or_update_many(entities=[CreateUserCmd(name="a")])

    path, payload = http.post.call_args.args
    assert path == "/api/v2/users/create_or_update_many"
    assert payload == {"users": [{"name": "a"}]}


def test_update_many_uniform(http, domain):
    http.put.return_value = {"job_status": {}}
    client = UserApiClient(http)

    client.update_many(user_ids=[1, 2], entity=UpdateUserCmd(role="agent"))

    path, payload = http.put.call_args.args
    assert path == "/api/v2/users/update_many?ids=1,2"
    assert payload == {"user": {"role": "agent"}}


def test_update_many_individually_embeds_ids(http, domain):
    http.put.return_value = {"job_status": {}}
    client = UserApiClient(http)

    client.update_many_individually(
        updates=[(1, UpdateUserCmd(role="admin")), (2, UpdateUserCmd(name="n"))]
    )

    path, payload = http.put.call_args.args
    assert path == "/api/v2/users/update_many"
    assert payload["users"][0]["id"] == 1
    assert payload["users"][0]["role"] == "admin"
    assert payload["users"][1]["id"] == 2
    assert payload["users"][1]["name"] == "n"


def test_destroy_many(http, domain):
    http.delete.return_value = {"job_status": {}}
    client = UserApiClient(http)

    client.destroy_many(user_ids=[5, 6])

    http.delete.assert_called_once_with("/api/v2/users/destroy_many?ids=5,6")


def test_destroy_many_empty_response(http, domain):
    http.delete.return_value = None
    client = UserApiClient(http)

    with pytest.raises(KeyError):
        client.destroy_many(user_ids=[1])


def test_merge_puts_target_user(http, domain):
    http.put.return_value = {"user": {}}
    client = UserApiClient(http)

    client.merge(source_user_id=1, target_user_id=2)

    path, payload = http.put.call_args.args
    assert path == "/api/v2/users/1/merge"
    assert payload == {"user": {"id": 2}}


# ---------------------------------------------------------------------------
# deleted users
# ---------------------------------------------------------------------------


def test_list_deleted(http, domain):
    http.get.return_value = {"deleted_users": []}
    client = UserApiClient(http)

    list(client.list_deleted())

    http.get.assert_called_with("/api/v2/deleted_users")


def test_count_deleted(http, mocker):
    http.get.return_value = {"count": {"value": 3}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_api_client.to_count_snapshot",
        return_value="snap",
    )
    client = UserApiClient(http)

    assert client.count_deleted() == "snap"
    http.get.assert_called_once_with("/api/v2/deleted_users/count")


def test_show_deleted(http, domain):
    http.get.return_value = {"deleted_user": {}}
    client = UserApiClient(http)

    client.show_deleted(deleted_user_id=11)

    http.get.assert_called_once_with("/api/v2/deleted_users/11")


def test_permanently_delete(http, domain):
    http.delete.return_value = {"deleted_user": {}}
    client = UserApiClient(http)

    client.permanently_delete(deleted_user_id=11)

    http.delete.assert_called_once_with("/api/v2/deleted_users/11")


def test_permanently_delete_empty_response(http, domain):
    http.delete.return_value = None
    client = UserApiClient(http)

    with pytest.raises(KeyError):
        client.permanently_delete(deleted_user_id=11)


# ---------------------------------------------------------------------------
# settings / entitlements / other misc
# ---------------------------------------------------------------------------


def test_me_settings_returns_nested_settings(http):
    http.get.return_value = {"settings": {"theme": "dark"}}
    client = UserApiClient(http)
    assert client.me_settings() == {"theme": "dark"}


def test_me_settings_falls_back_to_raw(http):
    http.get.return_value = {"theme": "dark"}
    client = UserApiClient(http)
    assert client.me_settings() == {"theme": "dark"}


def test_update_me_settings_puts_body(http):
    http.put.return_value = {"settings": {"theme": "light"}}
    client = UserApiClient(http)

    assert client.update_me_settings(settings={"theme": "light"}) == {"theme": "light"}
    http.put.assert_called_once_with(
        "/api/v2/users/me/settings", {"settings": {"theme": "light"}}
    )


def test_update_me_settings_falls_back_to_raw(http):
    http.put.return_value = {"ok": True}
    client = UserApiClient(http)

    assert client.update_me_settings(settings={}) == {"ok": True}


def test_list_entitlements(http):
    http.get.return_value = {"entitlements": [{"id": 1}]}
    client = UserApiClient(http)

    assert client.list_entitlements(user_id=5) == [{"id": 1}]
    http.get.assert_called_once_with("/api/v2/users/5/entitlements/full")


def test_list_entitlements_missing_key_returns_empty(http):
    http.get.return_value = {}
    client = UserApiClient(http)

    assert client.list_entitlements(user_id=5) == []


def test_request_create_returns_raw(http):
    http.post.return_value = {"status": "ok"}
    client = UserApiClient(http)

    result = client.request_create(entity=CreateUserCmd(name="n", email="e@x.y"))

    assert result == {"status": "ok"}
    http.post.assert_called_once_with(
        "/api/v2/users/request_create", {"user": {"name": "n", "email": "e@x.y"}}
    )


def test_logout_many_posts_empty_body(http):
    client = UserApiClient(http)

    client.logout_many(user_ids=[1, 2])

    http.post.assert_called_once_with("/api/v2/users/logout_many?ids=1,2", {})


# ---------------------------------------------------------------------------
# tags
# ---------------------------------------------------------------------------


def test_list_tags_returns_list(http):
    http.get.return_value = {"tags": ["a"]}
    client = UserApiClient(http)

    assert client.list_tags(user_id=5) == ["a"]
    http.get.assert_called_once_with("/api/v2/users/5/tags")


def test_list_tags_missing_key(http):
    http.get.return_value = {}
    client = UserApiClient(http)
    assert client.list_tags(user_id=5) == []


def test_set_tags(http):
    http.post.return_value = {"tags": ["a"]}
    client = UserApiClient(http)

    assert client.set_tags(user_id=5, tags=["a"]) == ["a"]
    http.post.assert_called_once_with("/api/v2/users/5/tags", {"tags": ["a"]})


def test_add_tags(http):
    http.put.return_value = {"tags": ["a", "b"]}
    client = UserApiClient(http)

    assert client.add_tags(user_id=5, tags=["b"]) == ["a", "b"]
    http.put.assert_called_once_with("/api/v2/users/5/tags", {"tags": ["b"]})


def test_remove_tags_sends_body_with_delete(http):
    http.delete.return_value = {"tags": ["a"]}
    client = UserApiClient(http)

    assert client.remove_tags(user_id=5, tags=["b"]) == ["a"]
    http.delete.assert_called_once_with("/api/v2/users/5/tags", json={"tags": ["b"]})


def test_remove_tags_handles_empty_response(http):
    http.delete.return_value = None
    client = UserApiClient(http)

    assert client.remove_tags(user_id=5, tags=["b"]) == []


# ---------------------------------------------------------------------------
# Iterator bodies: non-empty responses exercise the `yield to_domain(...)` path
# ---------------------------------------------------------------------------


def test_list_all_yields_domain_per_user(http, domain):
    http.get.return_value = {"users": [{"id": 1}, {"id": 2}]}
    client = UserApiClient(http)

    assert len(list(client.list_all())) == 2


def test_list_by_group_yields_domain(http, domain):
    http.get.return_value = {"users": [{"id": 1}]}
    client = UserApiClient(http)

    assert len(list(client.list_by_group(1))) == 1


def test_list_by_organization_yields_domain(http, domain):
    http.get.return_value = {"users": [{"id": 1}]}
    client = UserApiClient(http)

    assert len(list(client.list_by_organization(1))) == 1


def test_search_yields_domain(http, domain):
    http.get.return_value = {"users": [{"id": 1}]}
    client = UserApiClient(http)

    assert len(list(client.search(query="alice"))) == 1


def test_list_deleted_yields_domain(http, domain):
    http.get.return_value = {"deleted_users": [{"id": 1}]}
    client = UserApiClient(http)

    assert len(list(client.list_deleted())) == 1
