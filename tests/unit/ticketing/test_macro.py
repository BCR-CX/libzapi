import pytest

from libzapi.application.commands.ticketing.macro_cmds import (
    CreateMacroCmd,
    UpdateMacroCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import MacroApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.macro_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# Listing / pagination endpoints
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "method_name, expected_path",
    [
        ("list", "/api/v2/macros"),
        ("list_active", "/api/v2/macros/active"),
    ],
)
def test_macro_api_client_list_endpoints(method_name, expected_path, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"macros": []}

    client = MacroApiClient(https)
    list(getattr(client, method_name)())

    https.get.assert_called_with(expected_path)


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "macros": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = MacroApiClient(http)
    result = list(client.list())
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_list_active_yields_items(http, domain):
    http.get.return_value = {
        "macros": [{"id": 10}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = MacroApiClient(http)
    assert len(list(client.list_active())) == 1


def test_search_yields_items(http, domain):
    http.get.return_value = {
        "macros": [{"id": 7}, {"id": 8}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = MacroApiClient(http)
    result = list(client.search(query="libzapi"))
    http.get.assert_called_with("/api/v2/macros/search?query=libzapi")
    assert len(result) == 2


# ---------------------------------------------------------------------------
# Simple endpoints
# ---------------------------------------------------------------------------


def test_list_categories_returns_list(http):
    http.get.return_value = {"categories": ["a", "b"]}
    client = MacroApiClient(http)
    assert client.list_categories() == ["a", "b"]
    http.get.assert_called_with("/api/v2/macros/categories")


def test_list_categories_missing_key_returns_empty(http):
    http.get.return_value = {}
    client = MacroApiClient(http)
    assert client.list_categories() == []


def test_list_definitions_returns_dict(http):
    http.get.return_value = {"definitions": {"conditions": []}}
    client = MacroApiClient(http)
    assert client.list_definitions() == {"definitions": {"conditions": []}}
    http.get.assert_called_with("/api/v2/macros/definitions")


def test_get_returns_domain(http, domain):
    http.get.return_value = {"macro": {"id": 5}}
    client = MacroApiClient(http)
    result = client.get(macro_id=5)
    http.get.assert_called_with("/api/v2/macros/5")
    assert result["id"] == 5


def test_apply_returns_result_dict(http):
    http.get.return_value = {"result": {"ticket": {"id": 1}}}
    client = MacroApiClient(http)
    assert client.apply(macro_id=9) == {"ticket": {"id": 1}}
    http.get.assert_called_with("/api/v2/macros/9/apply")


def test_apply_returns_empty_when_missing(http):
    http.get.return_value = {}
    client = MacroApiClient(http)
    assert client.apply(macro_id=9) == {}


def test_apply_to_ticket_returns_result_dict(http):
    http.get.return_value = {"result": {"ticket": {"id": 3}}}
    client = MacroApiClient(http)
    assert client.apply_to_ticket(ticket_id=3, macro_id=9) == {"ticket": {"id": 3}}
    http.get.assert_called_with("/api/v2/tickets/3/macros/9/apply")


def test_apply_to_ticket_returns_empty_when_missing(http):
    http.get.return_value = {}
    client = MacroApiClient(http)
    assert client.apply_to_ticket(ticket_id=3, macro_id=9) == {}


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"macro": {"id": 1, "title": "Close"}}
    client = MacroApiClient(http)
    result = client.create(
        CreateMacroCmd(
            title="Close", actions=[{"field": "status", "value": "solved"}]
        )
    )
    http.post.assert_called_with(
        "/api/v2/macros",
        {
            "macro": {
                "title": "Close",
                "actions": [{"field": "status", "value": "solved"}],
            }
        },
    )
    assert result["title"] == "Close"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"macro": {"id": 1, "active": False}}
    client = MacroApiClient(http)
    client.update(macro_id=1, entity=UpdateMacroCmd(active=False))
    http.put.assert_called_with(
        "/api/v2/macros/1", {"macro": {"active": False}}
    )


def test_delete_calls_delete(http):
    client = MacroApiClient(http)
    client.delete(macro_id=7)
    http.delete.assert_called_with("/api/v2/macros/7")


# ---------------------------------------------------------------------------
# Bulk operations
# ---------------------------------------------------------------------------


def test_create_many_posts_list(http, domain):
    http.post.return_value = {"job_status": {"id": "abc"}}
    client = MacroApiClient(http)
    client.create_many(
        [
            CreateMacroCmd(title="A", actions=[{"field": "status", "value": "solved"}]),
            CreateMacroCmd(title="B", actions=[{"field": "priority", "value": "low"}]),
        ]
    )
    http.post.assert_called_with(
        "/api/v2/macros/create_many",
        {
            "macros": [
                {"title": "A", "actions": [{"field": "status", "value": "solved"}]},
                {"title": "B", "actions": [{"field": "priority", "value": "low"}]},
            ]
        },
    )


def test_update_many_puts_bodies_with_ids(http, domain):
    http.put.return_value = {"job_status": {"id": "abc"}}
    client = MacroApiClient(http)
    client.update_many(
        [
            (1, UpdateMacroCmd(active=False)),
            (2, UpdateMacroCmd(description="n")),
        ]
    )
    http.put.assert_called_with(
        "/api/v2/macros/update_many",
        {
            "macros": [
                {"active": False, "id": 1},
                {"description": "n", "id": 2},
            ]
        },
    )


def test_destroy_many_deletes_with_ids(http, domain):
    http.delete.return_value = {"job_status": {"id": "abc"}}
    client = MacroApiClient(http)
    client.destroy_many([1, 2])
    http.delete.assert_called_with("/api/v2/macros/destroy_many?ids=1,2")


def test_destroy_many_handles_none_response(http, domain):
    http.delete.return_value = None
    client = MacroApiClient(http)
    with pytest.raises(KeyError):
        client.destroy_many([1])


# ---------------------------------------------------------------------------
# Domain helpers
# ---------------------------------------------------------------------------


def test_macro_logical_key_normalises_title():
    from datetime import datetime

    from libzapi.domain.models.ticketing.macro import Macro

    macro = Macro(
        id=1,
        url="https://x",
        title="Close Ticket",
        active=True,
        updated_at=datetime.now(),
        created_at=datetime.now(),
        default=False,
        position=1,
        description="",
        actions=[],
        raw_title="Close Ticket",
    )
    assert macro.logical_key.as_str() == "macro:close_ticket"


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_macro_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = MacroApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
