import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def test_list_requests(ticketing: Ticketing):
    requests = list(itertools.islice(ticketing.requests.list_all(), 5))
    assert isinstance(requests, list)


def test_create_update_and_solve(ticketing: Ticketing):
    suffix = _unique()
    req = ticketing.requests.create(
        subject=f"libzapi request {suffix}",
        comment={"body": "created by libzapi"},
    )
    assert req.id > 0

    updated = ticketing.requests.update(
        req.id, comment={"body": "updated via libzapi", "public": False}
    )
    assert updated.id == req.id

    solved = ticketing.requests.update(req.id, solved=True)
    assert solved.status == "solved"


def test_list_comments(ticketing: Ticketing):
    req = ticketing.requests.create(
        subject=f"libzapi comments {_unique()}",
        comment={"body": "first comment"},
    )
    comments = list(ticketing.requests.list_comments(req.id))
    assert len(comments) >= 1
    first = ticketing.requests.get_comment(req.id, comments[0]["id"])
    assert first["id"] == comments[0]["id"]
