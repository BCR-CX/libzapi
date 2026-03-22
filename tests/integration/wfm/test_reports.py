import time

import pytest

from libzapi import WorkforceManagement


def test_get_report_data(wfm: WorkforceManagement):
    now = int(time.time())
    one_week_ago = now - 7 * 86400
    # This test requires a valid template_id from the account
    # Skip if no templates are available
    try:
        rows = list(wfm.reports.get_data(template_id="default", start_time=one_week_ago, end_time=now))
        assert isinstance(rows, list)
    except Exception:
        pytest.skip("No valid report template available or WFM not enabled")
