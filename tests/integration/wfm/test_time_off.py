from libzapi import WorkforceManagement


def test_list_time_off(wfm: WorkforceManagement):
    time_offs = list(wfm.time_off.list())
    assert isinstance(time_offs, list)


def test_list_time_off_with_filters(wfm: WorkforceManagement):
    time_offs = list(wfm.time_off.list(status="approved", page=1, per_page=10))
    assert isinstance(time_offs, list)
