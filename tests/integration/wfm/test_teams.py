import uuid

import pytest

from libzapi import WorkforceManagement


def test_list_teams(wfm: WorkforceManagement):
    teams = list(wfm.teams.list())
    assert isinstance(teams, list)


def test_list_and_get_team(wfm: WorkforceManagement):
    teams = list(wfm.teams.list())
    if not teams:
        pytest.skip("No teams found in the live API")
    team = wfm.teams.get(teams[0].id)
    assert team.id == teams[0].id


def test_create_update_delete_restore_team(wfm: WorkforceManagement):
    random_id = str(uuid.uuid4())[:8]
    team = wfm.teams.create(
        name=f"Test Team {random_id}",
        description="Integration test team",
        manager_id=0,
        agents_ids=[],
    )
    assert team.id is not None

    try:
        updated = wfm.teams.update(team.id, name=f"Updated Team {random_id}")
        assert updated.name == f"Updated Team {random_id}"

        fetched = wfm.teams.get(team.id)
        assert fetched.id == team.id
    finally:
        wfm.teams.delete(team.id)
