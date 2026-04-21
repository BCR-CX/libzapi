import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.application.commands.ticketing.ticket_cmds import (
    CreateTicketCmd,
    MergeTicketsCmd,
    UpdateTicketCmd,
)
from libzapi.domain.models.ticketing.ticket import Ticket, User
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import TicketApiClient

strategy = builds(
    Ticket,
    id=just(222),
)


@given(strategy)
def test_logical_key_from_id(ticket):
    assert ticket.logical_key.as_str() == "ticket:222"


def test_user_props():
    user = User(
        id=123,
        name="John Doe",
    )

    assert user.id == 123
    assert user.name == "John Doe"


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list", [], "/api/v2/tickets", "tickets"),
        ("list_organization", [456], "/api/v2/organizations/456/tickets", "tickets"),
        ("list_user_requested", [789], "/api/v2/users/789/tickets/requested", "tickets"),
        ("list_user_ccd", [101], "/api/v2/users/101/tickets/ccd", "tickets"),
        ("list_user_followed", [112], "/api/v2/users/112/tickets/followed", "tickets"),
        ("list_user_assigned", [131], "/api/v2/users/131/tickets/assigned", "tickets"),
        ("list_recent", [], "/api/v2/tickets/recent", "tickets"),
        ("list_collaborators", [141], "/api/v2/tickets/141/collaborators", "users"),
        ("list_followers", [151], "/api/v2/tickets/151/followers", "users"),
        ("list_email_ccs", [161], "/api/v2/tickets/161/email_ccs", "users"),
        ("list_incidents", [171], "/api/v2/tickets/171/incidents", "tickets"),
        ("list_problems", [], "/api/v2/tickets/problems", "tickets"),
        ("count", [], "/api/v2/tickets/count", "count"),
        ("organization_count", [201], "/api/v2/organizations/201/tickets/count", "count"),
        ("user_ccd_count", [211], "/api/v2/users/211/tickets/ccd/count", "count"),
        ("user_assigned_count", [221], "/api/v2/users/221/tickets/assigned/count", "count"),
        ("show_multiple_tickets", [[231, 232, 233]], "/api/v2/tickets/show_many?ids=231,232,233", "tickets"),
    ],
)
def test_ticket_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = TicketApiClient(https)

    method = getattr(client, method_name, None)
    list(method(*args))

    https.get.assert_called_with(expected_path)


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_ticket_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = TicketApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())


# ---------------------------------------------------------------------------
# create / update / create_many / update_many_*
# ---------------------------------------------------------------------------


@pytest.fixture
def http(mocker):
    stub = mocker.Mock()
    stub.base_url = "https://example.zendesk.com"
    return stub


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_api_client.to_domain",
        return_value=mocker.Mock(),
    )


def test_create_ticket_posts_mapped_payload(http, domain):
    http.post.return_value = {"ticket": {"id": 1}}
    client = TicketApiClient(http)

    cmd = CreateTicketCmd(subject="s", custom_fields=[], description="d")
    client.create_ticket(entity=cmd)

    path, payload = http.post.call_args.args
    assert path == "/api/v2/tickets"
    assert payload["ticket"]["subject"] == "s"


def test_update_ticket_puts_to_path(http, domain):
    http.put.return_value = {"ticket": {"id": 42}}
    client = TicketApiClient(http)

    client.update_ticket(ticket_id=42, entity=UpdateTicketCmd(subject="new"))

    path, payload = http.put.call_args.args
    assert path == "/api/v2/tickets/42"
    assert payload["ticket"] == {"subject": "new"}


def test_create_many_posts_list_payload(http, domain):
    http.post.return_value = {"job_status": {"id": "abc"}}
    client = TicketApiClient(http)

    client.create_many(
        entity=[
            CreateTicketCmd(subject="a", custom_fields=[], description="d"),
            CreateTicketCmd(subject="b", custom_fields=[], description="d"),
        ]
    )

    path, payload = http.post.call_args.args
    assert path == "/api/v2/tickets/create_many"
    assert len(payload["tickets"]) == 2


def test_update_many_builds_ids_query(http, domain):
    http.put.return_value = {"job_status": {"id": "j"}}
    client = TicketApiClient(http)

    client.update_many(ticket_ids=[1, 2, 3], entity=UpdateTicketCmd(priority="low"))

    path, _ = http.put.call_args.args
    assert path == "/api/v2/tickets/update_many?ids=1,2,3"


def test_update_many_individually_embeds_ids_in_payload(http, domain):
    http.put.return_value = {"job_status": {"id": "j"}}
    client = TicketApiClient(http)

    client.update_many_individually(
        updates=[(1, UpdateTicketCmd(priority="low")), (2, UpdateTicketCmd(subject="x"))]
    )

    path, payload = http.put.call_args.args
    assert path == "/api/v2/tickets/update_many"
    assert payload["tickets"][0]["id"] == 1
    assert payload["tickets"][1]["id"] == 2


# ---------------------------------------------------------------------------
# delete / destroy_many / restore / permanently_delete
# ---------------------------------------------------------------------------


def test_delete_calls_delete_path(http):
    client = TicketApiClient(http)
    client.delete(ticket_id=42)
    http.delete.assert_called_once_with("/api/v2/tickets/42")


def test_destroy_many_joins_ids(http, domain):
    http.delete.return_value = {"job_status": {"id": "j"}}
    client = TicketApiClient(http)

    client.destroy_many(ticket_ids=[5, 6])

    http.delete.assert_called_once_with("/api/v2/tickets/destroy_many?ids=5,6")


def test_destroy_many_handles_empty_body(http, domain):
    http.delete.return_value = None
    client = TicketApiClient(http)

    with pytest.raises(KeyError):
        client.destroy_many(ticket_ids=[1])


def test_mark_as_spam_puts_empty_body(http):
    client = TicketApiClient(http)
    client.mark_as_spam(ticket_id=5)
    http.put.assert_called_once_with("/api/v2/tickets/5/mark_as_spam", {})


def test_mark_many_as_spam(http, domain):
    http.put.return_value = {"job_status": {"id": "j"}}
    client = TicketApiClient(http)

    client.mark_many_as_spam(ticket_ids=[1, 2])

    http.put.assert_called_once_with("/api/v2/tickets/mark_many_as_spam?ids=1,2", {})


def test_restore_puts_empty_body(http):
    client = TicketApiClient(http)
    client.restore(ticket_id=7)
    http.put.assert_called_once_with("/api/v2/deleted_tickets/7/restore", {})


def test_restore_many_puts_empty_body(http):
    client = TicketApiClient(http)
    client.restore_many(ticket_ids=[1, 2])
    http.put.assert_called_once_with("/api/v2/deleted_tickets/restore_many?ids=1,2", {})


def test_permanently_delete(http, domain):
    http.delete.return_value = {"job_status": {"id": "j"}}
    client = TicketApiClient(http)

    client.permanently_delete(ticket_id=7)

    http.delete.assert_called_once_with("/api/v2/deleted_tickets/7")


def test_permanently_delete_many(http, domain):
    http.delete.return_value = {"job_status": {"id": "j"}}
    client = TicketApiClient(http)

    client.permanently_delete_many(ticket_ids=[1, 2])

    http.delete.assert_called_once_with("/api/v2/deleted_tickets/destroy_many?ids=1,2")


# ---------------------------------------------------------------------------
# merge / related / list_deleted / problems_autocomplete
# ---------------------------------------------------------------------------


def test_merge_posts_mapped_payload(http, domain):
    http.post.return_value = {"job_status": {"id": "j"}}
    client = TicketApiClient(http)

    client.merge(
        target_ticket_id=10,
        entity=MergeTicketsCmd(source_ids=[1, 2], target_comment="hi"),
    )

    path, payload = http.post.call_args.args
    assert path == "/api/v2/tickets/10/merge"
    assert payload["ids"] == [1, 2]
    assert payload["target_comment"] == "hi"


def test_list_related(http, domain):
    http.get.return_value = {"ticket_related": {"incidents": 3}}
    client = TicketApiClient(http)

    client.list_related(ticket_id=42)

    http.get.assert_called_once_with("/api/v2/tickets/42/related")


def test_list_deleted_paginates(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"deleted_tickets": []}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    client = TicketApiClient(https)

    list(client.list_deleted())

    https.get.assert_called_with("/api/v2/deleted_tickets")


def test_problems_autocomplete_posts_text(http, domain):
    http.post.return_value = {"tickets": [{"id": 1, "subject": "net"}]}
    client = TicketApiClient(http)

    list(client.problems_autocomplete(text="net"))

    path, payload = http.post.call_args.args
    assert path == "/api/v2/problems/autocomplete"
    assert payload == {"text": "net"}


# ---------------------------------------------------------------------------
# ticket tags
# ---------------------------------------------------------------------------


def test_list_tags_returns_list(http):
    http.get.return_value = {"tags": ["a", "b"]}
    client = TicketApiClient(http)

    assert client.list_tags(ticket_id=5) == ["a", "b"]
    http.get.assert_called_once_with("/api/v2/tickets/5/tags")


def test_list_tags_missing_key_returns_empty(http):
    http.get.return_value = {}
    client = TicketApiClient(http)

    assert client.list_tags(ticket_id=5) == []


def test_set_tags_posts_body(http):
    http.post.return_value = {"tags": ["a"]}
    client = TicketApiClient(http)

    assert client.set_tags(ticket_id=5, tags=["a"]) == ["a"]
    http.post.assert_called_once_with("/api/v2/tickets/5/tags", {"tags": ["a"]})


def test_add_tags_puts_body(http):
    http.put.return_value = {"tags": ["a", "b"]}
    client = TicketApiClient(http)

    assert client.add_tags(ticket_id=5, tags=["b"]) == ["a", "b"]
    http.put.assert_called_once_with("/api/v2/tickets/5/tags", {"tags": ["b"]})


def test_remove_tags_sends_body_with_delete(http):
    http.delete.return_value = {"tags": ["a"]}
    client = TicketApiClient(http)

    assert client.remove_tags(ticket_id=5, tags=["b"]) == ["a"]
    http.delete.assert_called_once_with("/api/v2/tickets/5/tags", json={"tags": ["b"]})


def test_remove_tags_handles_empty_response(http):
    http.delete.return_value = None
    client = TicketApiClient(http)

    assert client.remove_tags(ticket_id=5, tags=["b"]) == []


# ---------------------------------------------------------------------------
# Iterator bodies: non-empty responses exercise the `yield to_domain(...)` path
# ---------------------------------------------------------------------------


def test_list_yields_item_per_ticket(http, domain, mocker):
    http.get.return_value = {"tickets": [{"id": 1}]}
    domain.return_value = mocker.Mock()
    client = TicketApiClient(http)

    assert len(list(client.list())) == 1


def test_get_calls_to_domain(http, domain):
    http.get.return_value = {"ticket": {"id": 1}}
    client = TicketApiClient(http)

    client.get(ticket_id=1)
    domain.assert_called_once()


def test_collaborator_endpoints_yield_users(http, domain):
    http.get.return_value = {"users": [{"id": 1}]}
    client = TicketApiClient(http)

    assert len(list(client.list_collaborators(ticket_id=1))) == 1
    assert len(list(client.list_followers(ticket_id=1))) == 1
    assert len(list(client.list_email_ccs(ticket_id=1))) == 1


def test_show_multiple_tickets_yields_each(http, domain):
    http.get.return_value = {"tickets": [{"id": 1}, {"id": 2}]}
    client = TicketApiClient(http)

    assert len(list(client.show_multiple_tickets(ticket_ids=[1, 2]))) == 2
