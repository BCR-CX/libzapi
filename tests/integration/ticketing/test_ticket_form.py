import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _pick_a_field_id(ticketing: Ticketing) -> int:
    return next(iter(ticketing.ticket_fields.list_all())).id


def _create_form(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        name=f"libzapi form {suffix}",
        ticket_field_ids=[_pick_a_field_id(ticketing)],
    )
    defaults.update(overrides)
    return ticketing.ticket_forms.create(**defaults)


def test_list_and_get_ticket_form(ticketing: Ticketing):
    forms = list(itertools.islice(ticketing.ticket_forms.list_all(), 20))
    assert len(forms) > 0
    form = ticketing.ticket_forms.get_by_id(forms[0].id)
    assert form.name == forms[0].name


def test_create_update_delete_form(ticketing: Ticketing):
    form = _create_form(ticketing, end_user_visible=False)
    assert form.id > 0
    try:
        updated = ticketing.ticket_forms.update(
            form.id, display_name="libzapi updated", active=False
        )
        assert updated.active is False
    finally:
        ticketing.ticket_forms.delete(form.id)


def test_clone_form(ticketing: Ticketing):
    form = _create_form(ticketing)
    try:
        clone = ticketing.ticket_forms.clone(form.id)
        try:
            assert clone.id != form.id
        finally:
            ticketing.ticket_forms.delete(clone.id)
    finally:
        ticketing.ticket_forms.delete(form.id)


def test_reorder_does_not_raise(ticketing: Ticketing):
    forms = list(itertools.islice(ticketing.ticket_forms.list_all(), 5))
    ids = [f.id for f in forms]
    ticketing.ticket_forms.reorder(ids)
