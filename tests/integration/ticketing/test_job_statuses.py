import itertools

import pytest

from libzapi import Ticketing


def test_list_all(ticketing: Ticketing):
    items = list(itertools.islice(ticketing.job_statuses.list_all(), 20))
    assert isinstance(items, list)


def test_get_unknown_raises(ticketing: Ticketing):
    from libzapi.domain.errors import NotFound

    with pytest.raises(NotFound):
        ticketing.job_statuses.get_by_id("this-job-does-not-exist-" + "0" * 20)


def test_wait_until_complete_on_known_job(ticketing: Ticketing):
    jobs = list(itertools.islice(ticketing.job_statuses.list_all(), 5))
    if not jobs:
        pytest.skip("No job statuses available on this tenant.")
    finished = [
        j for j in jobs if j.status in {"completed", "failed", "killed"}
    ]
    if not finished:
        pytest.skip("No terminal job statuses available on this tenant.")
    target = finished[0]
    result = ticketing.job_statuses.wait_until_complete(
        target.id, interval=0.5, timeout=5.0
    )
    assert result.id == target.id
    assert result.status in {"completed", "failed", "killed"}
