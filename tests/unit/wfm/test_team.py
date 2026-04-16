import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.application.commands.wfm.team_cmds import BulkAgentsCmd, CreateTeamCmd, UpdateTeamCmd
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.wfm.team import Team
from libzapi.infrastructure.api_clients.wfm import TeamApiClient

MODULE = "libzapi.infrastructure.api_clients.wfm.team_api_client"

strategy = builds(Team, id=just("team-1"), name=just("Support"))


@given(strategy)
def test_logical_key(model: Team):
    assert model.logical_key.as_str() == "wfm_team:support"


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"teams": [{}]}
    client = TeamApiClient(https)
    list(client.list())
    https.get.assert_called_with("/wfm/l5/api/v2/teams")


def test_list_with_deleted(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"teams": [{}]}
    client = TeamApiClient(https)
    list(client.list(deleted=True))
    https.get.assert_called_with("/wfm/l5/api/v2/teams?deleted=true")


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {}
    client = TeamApiClient(https)
    client.get("team-1")
    https.get.assert_called_with("/wfm/l5/api/v2/teams/team-1")


def test_create(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(
        f"{MODULE}.to_payload_create",
        return_value={"name": "T", "description": "D", "manager_id": 1, "agents_ids": []},
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {}
    client = TeamApiClient(https)
    cmd = CreateTeamCmd(name="T", description="D", manager_id=1, agents_ids=[])
    client.create(cmd=cmd)
    https.post.assert_called_with(
        "/wfm/l5/api/v2/teams",
        json={"name": "T", "description": "D", "manager_id": 1, "agents_ids": []},
    )


def test_update(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"name": "New"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {}
    client = TeamApiClient(https)
    cmd = UpdateTeamCmd(name="New")
    client.update("team-1", cmd=cmd)
    https.put.assert_called_with("/wfm/l5/api/v2/teams/team-1", json={"name": "New"})


def test_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = TeamApiClient(https)
    client.delete("team-1")
    https.delete.assert_called_with("/wfm/l5/api/v2/teams/team-1")


def test_restore(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {}
    client = TeamApiClient(https)
    client.restore("team-1")
    https.post.assert_called_with("/wfm/l5/api/v2/teams/restore", json={"id": "team-1"})


def test_bulk_add_agents(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(
        f"{MODULE}.to_payload_bulk_agents",
        return_value={"agent_ids": ["a1"], "team_ids": ["t1"]},
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {}
    client = TeamApiClient(https)
    cmd = BulkAgentsCmd(agent_ids=["a1"], team_ids=["t1"])
    client.bulk_add_agents(cmd=cmd)
    https.post.assert_called_with(
        "/wfm/l5/api/v2/teams/bulk/add_agents",
        json={"agent_ids": ["a1"], "team_ids": ["t1"]},
    )


def test_bulk_remove_agents(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(
        f"{MODULE}.to_payload_bulk_agents",
        return_value={"agent_ids": ["a1"], "team_ids": ["t1"]},
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {}
    client = TeamApiClient(https)
    cmd = BulkAgentsCmd(agent_ids=["a1"], team_ids=["t1"])
    client.bulk_remove_agents(cmd=cmd)
    https.post.assert_called_with(
        "/wfm/l5/api/v2/teams/bulk/remove_agents",
        json={"agent_ids": ["a1"], "team_ids": ["t1"]},
    )


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.get.side_effect = error_cls("error")
    client = TeamApiClient(https)
    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.get.side_effect = error_cls("error")
    client = TeamApiClient(https)
    with pytest.raises(error_cls):
        client.get("team-1")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_create_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.post.side_effect = error_cls("error")
    client = TeamApiClient(https)
    cmd = CreateTeamCmd(name="T", description="D", manager_id=1, agents_ids=[])
    with pytest.raises(error_cls):
        client.create(cmd=cmd)


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.delete.side_effect = error_cls("error")
    client = TeamApiClient(https)
    with pytest.raises(error_cls):
        client.delete("team-1")
