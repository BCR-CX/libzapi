from datetime import date, timedelta


from libzapi import WorkforceManagement


def test_fetch_shifts(wfm: WorkforceManagement):
    today = date.today()
    start = (today - timedelta(days=7)).isoformat()
    end = today.isoformat()
    shifts = list(wfm.shifts.fetch(start_date=start, end_date=end))
    assert isinstance(shifts, list)
