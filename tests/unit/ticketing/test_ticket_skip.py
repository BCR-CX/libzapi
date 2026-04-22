import pytest

from libzapi.application.commands.ticketing.ticket_skip_cmds import CreateTicketSkipCmd
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import TicketSkipApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_skip_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.mark.parametrize(
    "method, args, path",
    [
        ("list", [], "/api/v2/skips"),
        ("list_by_user", [42], "/api/v2/users/42/skips"),
        ("list_by_ticket", [7], "/api/v2/tickets/7/skips"),
    ],
)
def test_list_endpoints_hit_expected_path(method, args, path, http, domain):
    http.get.return_value = {"skips": [{"id": 1}]}
    client = TicketSkipApiClient(http)
    items = list(getattr(client, method)(*args))
    assert len(items) == 1
    assert items[0]["_cls"] == "TicketSkip"
    http.get.assert_called_with(path)


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "skips": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = TicketSkipApiClient(http)
    items = list(client.list())
    assert len(items) == 2
    assert all(i["_cls"] == "TicketSkip" for i in items)


def test_list_by_user_coerces_user_id(http, domain):
    http.get.return_value = {"skips": []}
    client = TicketSkipApiClient(http)
    list(client.list_by_user(user_id="5"))  # type: ignore[arg-type]
    http.get.assert_called_with("/api/v2/users/5/skips")


def test_create_posts_payload(http, domain):
    http.post.return_value = {"skip": {"id": 1}}
    client = TicketSkipApiClient(http)
    client.create(ticket_id=42, entity=CreateTicketSkipCmd(reason="not my area"))
    http.post.assert_called_with(
        "/api/v2/tickets/42/skips", {"skip": {"reason": "not my area"}}
    )


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = TicketSkipApiClient(http)
    with pytest.raises(error_cls):
        list(client.list())


def test_ticket_skip_logical_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.ticket_skip import TicketSkip

    skip = TicketSkip(
        id=9,
        user_id=42,
        ticket_id=7,
        reason="not mine",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert skip.logical_key.as_str() == "ticket_skip:skip_id_9"
