from datetime import datetime

from libzapi.domain.models.ticketing.comment import Comment


def test_comment_logical_key():
    c = Comment(
        id=42,
        type="Comment",
        author_id=1,
        body="hello",
        html_body="<p>hello</p>",
        plain_body="hello",
        public=True,
        created_at=datetime(2026, 1, 1),
    )
    assert c.logical_key.as_str() == "ticket_comment:comment_id_42"


def test_comment_defaults_are_empty():
    c = Comment(
        id=1,
        type="Comment",
        author_id=1,
        body="x",
        html_body="x",
        plain_body="x",
        public=False,
        created_at=datetime(2026, 1, 1),
    )
    assert c.attachments == []
    assert c.via is None
    assert c.metadata is None
    assert c.audit_id is None
