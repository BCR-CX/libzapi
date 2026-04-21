import uuid

from libzapi import Ticketing


def _make_ticket(ticketing: Ticketing, suffix: str = ""):
    tag = f"libzapi-{uuid.uuid4().hex[:8]}{suffix}"
    return ticketing.tickets.create(
        subject=f"libzapi integration {tag}",
        description=f"integration test ticket {tag}",
    )


def test_list_and_get(ticketing: Ticketing):
    items = list(ticketing.tickets.list())
    assert len(items) > 0
    item = ticketing.tickets.get(items[0].id)
    assert item.id == items[0].id


def test_create_and_update_ticket(ticketing: Ticketing):
    fields = list(ticketing.ticket_fields.list_all())
    custom_fields = [{"id": f.id, "value": "Test value"} for f in fields[:2] if f.type == "text"]

    ticket = ticketing.tickets.create(
        subject="Test ticket",
        description="Test ticket description",
        custom_fields=custom_fields,
    )
    assert ticket.subject == "Test ticket"
    updated_ticket = ticketing.tickets.update(ticket_id=ticket.id, subject="Updated ticket")
    assert updated_ticket.subject == "Updated ticket"


def test_create_many(ticketing: Ticketing):
    many = ticketing.tickets.create_many(
        [
            {"subject": "Test ticket 1", "description": "Test ticket description 1"},
            {"subject": "Test ticket 2", "description": "Test ticket description 2"},
        ]
    )
    assert many.total == 2


def test_delete_ticket(ticketing: Ticketing):
    ticket = _make_ticket(ticketing)
    ticketing.tickets.delete(ticket.id)
    deleted_ids = {t.id for t in ticketing.tickets.list_deleted()}
    assert ticket.id in deleted_ids


def test_destroy_many(ticketing: Ticketing):
    a = _make_ticket(ticketing, "-a")
    b = _make_ticket(ticketing, "-b")
    job = ticketing.tickets.destroy_many([a.id, b.id])
    assert job.id


def test_update_many_uniform(ticketing: Ticketing):
    a = _make_ticket(ticketing, "-uma")
    b = _make_ticket(ticketing, "-umb")
    job = ticketing.tickets.update_many(
        [a.id, b.id], tags=["libzapi-update-many"]
    )
    assert job.id


def test_update_many_individually(ticketing: Ticketing):
    a = _make_ticket(ticketing, "-umia")
    b = _make_ticket(ticketing, "-umib")
    job = ticketing.tickets.update_many_individually(
        [(a.id, {"tags": ["libzapi-tag-a"]}), (b.id, {"tags": ["libzapi-tag-b"]})]
    )
    assert job.id


def test_mark_as_spam(ticketing: Ticketing):
    ticket = _make_ticket(ticketing, "-spam")
    ticketing.tickets.mark_as_spam(ticket.id)


def test_mark_many_as_spam(ticketing: Ticketing):
    a = _make_ticket(ticketing, "-mms-a")
    b = _make_ticket(ticketing, "-mms-b")
    job = ticketing.tickets.mark_many_as_spam([a.id, b.id])
    assert job.id


def test_merge_tickets(ticketing: Ticketing):
    target = _make_ticket(ticketing, "-merge-target")
    source_a = _make_ticket(ticketing, "-merge-src-a")
    source_b = _make_ticket(ticketing, "-merge-src-b")
    job = ticketing.tickets.merge(
        target_ticket_id=target.id,
        source_ids=[source_a.id, source_b.id],
        target_comment="merged from libzapi test",
        source_comment="merged into target from libzapi test",
    )
    assert job.id


def test_list_related(ticketing: Ticketing):
    ticket = _make_ticket(ticketing, "-related")
    related = ticketing.tickets.list_related(ticket.id)
    assert related.incidents == 0


def test_list_deleted(ticketing: Ticketing):
    ticket = _make_ticket(ticketing, "-list-del")
    ticketing.tickets.delete(ticket.id)
    deleted = list(ticketing.tickets.list_deleted())
    assert any(t.id == ticket.id for t in deleted)


def test_restore_ticket(ticketing: Ticketing):
    ticket = _make_ticket(ticketing, "-restore")
    ticketing.tickets.delete(ticket.id)
    ticketing.tickets.restore(ticket.id)
    restored = ticketing.tickets.get(ticket.id)
    assert restored.id == ticket.id


def test_restore_many(ticketing: Ticketing):
    a = _make_ticket(ticketing, "-rm-a")
    b = _make_ticket(ticketing, "-rm-b")
    ticketing.tickets.delete(a.id)
    ticketing.tickets.delete(b.id)
    ticketing.tickets.restore_many([a.id, b.id])
    assert ticketing.tickets.get(a.id).id == a.id
    assert ticketing.tickets.get(b.id).id == b.id


def test_permanently_delete(ticketing: Ticketing):
    ticket = _make_ticket(ticketing, "-perm-del")
    ticketing.tickets.delete(ticket.id)
    job = ticketing.tickets.permanently_delete(ticket.id)
    assert job.id


def test_permanently_delete_many(ticketing: Ticketing):
    a = _make_ticket(ticketing, "-pdm-a")
    b = _make_ticket(ticketing, "-pdm-b")
    ticketing.tickets.delete(a.id)
    ticketing.tickets.delete(b.id)
    job = ticketing.tickets.permanently_delete_many([a.id, b.id])
    assert job.id


def test_problems_autocomplete(ticketing: Ticketing):
    problem = ticketing.tickets.create(
        subject="libzapi problem autocomplete seed",
        description="seed for autocomplete",
        ticket_type="problem",
    )
    matches = list(ticketing.tickets.problems_autocomplete(text="libzapi"))
    assert any(m.id == problem.id for m in matches) or matches == []


def test_list_tags(ticketing: Ticketing):
    ticket = ticketing.tickets.create(
        subject="libzapi list_tags",
        description="list tags test",
        tags=["libzapi-listtags"],
    )
    tags = ticketing.tickets.list_tags(ticket.id)
    assert "libzapi-listtags" in tags


def test_set_tags(ticketing: Ticketing):
    ticket = _make_ticket(ticketing, "-settags")
    tags = ticketing.tickets.set_tags(ticket.id, ["libzapi-set-a", "libzapi-set-b"])
    assert set(tags) >= {"libzapi-set-a", "libzapi-set-b"}


def test_add_tags(ticketing: Ticketing):
    ticket = ticketing.tickets.create(
        subject="libzapi add_tags",
        description="add tags test",
        tags=["libzapi-keep"],
    )
    tags = ticketing.tickets.add_tags(ticket.id, ["libzapi-added"])
    assert {"libzapi-keep", "libzapi-added"} <= set(tags)


def test_remove_tags(ticketing: Ticketing):
    ticket = ticketing.tickets.create(
        subject="libzapi remove_tags",
        description="remove tags test",
        tags=["libzapi-keep", "libzapi-drop"],
    )
    tags = ticketing.tickets.remove_tags(ticket.id, ["libzapi-drop"])
    assert "libzapi-drop" not in tags
    assert "libzapi-keep" in tags
