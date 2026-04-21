import pytest

from libzapi.application.commands.ticketing.workspace_cmds import (
    CreateWorkspaceCmd,
    UpdateWorkspaceCmd,
)
from libzapi.domain.errors import (
    NotFound,
    RateLimited,
    Unauthorized,
    UnprocessableEntity,
)
from libzapi.infrastructure.api_clients.ticketing import WorkspaceApiClient


_COND = {"all": [{"field": "status", "operator": "is", "value": "new"}]}


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.workspace_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "workspaces": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = WorkspaceApiClient(http)
    result = list(client.list())
    http.get.assert_called_with("/api/v2/workspaces")
    assert len(result) == 2


def test_get_returns_domain(http, domain):
    http.get.return_value = {"workspace": {"id": 5}}
    client = WorkspaceApiClient(http)
    result = client.get(workspace_id=5)
    http.get.assert_called_with("/api/v2/workspaces/5")
    assert result["id"] == 5


def test_create_posts_payload(http, domain):
    http.post.return_value = {"workspace": {"id": 1, "title": "W"}}
    client = WorkspaceApiClient(http)
    result = client.create(CreateWorkspaceCmd(title="W", conditions=_COND))
    http.post.assert_called_with(
        "/api/v2/workspaces",
        {"workspace": {"title": "W", "conditions": _COND}},
    )
    assert result["title"] == "W"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"workspace": {"id": 1, "activated": False}}
    client = WorkspaceApiClient(http)
    client.update(workspace_id=1, entity=UpdateWorkspaceCmd(activated=False))
    http.put.assert_called_with(
        "/api/v2/workspaces/1", {"workspace": {"activated": False}}
    )


def test_delete_calls_delete(http):
    client = WorkspaceApiClient(http)
    client.delete(workspace_id=7)
    http.delete.assert_called_with("/api/v2/workspaces/7")


def test_destroy_many_deletes_with_ids(http):
    client = WorkspaceApiClient(http)
    client.destroy_many([1, 2])
    http.delete.assert_called_with("/api/v2/workspaces/destroy_many?ids=1,2")


def test_reorder_puts_ids(http):
    client = WorkspaceApiClient(http)
    client.reorder([3, 1, 2])
    http.put.assert_called_with(
        "/api/v2/workspaces/reorder", {"ids": [3, 1, 2]}
    )


def test_reorder_converts_iterable(http):
    client = WorkspaceApiClient(http)
    client.reorder(iter([3, 1]))
    http.put.assert_called_with("/api/v2/workspaces/reorder", {"ids": [3, 1]})


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_workspace_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = WorkspaceApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
