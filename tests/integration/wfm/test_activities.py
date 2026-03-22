import time


from libzapi import WorkforceManagement


def test_list_activities(wfm: WorkforceManagement):
    one_day_ago = int(time.time()) - 86400
    activities = list(wfm.activities.list(start_time=one_day_ago))
    assert isinstance(activities, list)


def test_list_activities_with_relationships(wfm: WorkforceManagement):
    one_day_ago = int(time.time()) - 86400
    activities, agents, activity_types = wfm.activities.list_with_relationships(start_time=one_day_ago)
    assert isinstance(activities, list)
    assert isinstance(agents, list)
    assert isinstance(activity_types, list)
