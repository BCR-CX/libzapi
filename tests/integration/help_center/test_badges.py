import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_badges(help_center: HelpCenter):
    try:
        badges = list(help_center.badges.list_all())
    except NotFound:
        pytest.skip("Gather badges not enabled on this account")
    assert isinstance(badges, list)


def test_list_badge_categories(help_center: HelpCenter):
    try:
        categories = list(help_center.badge_categories.list_all())
    except NotFound:
        pytest.skip("Gather badge categories not enabled on this account")
    assert isinstance(categories, list)


def test_list_badge_assignments(help_center: HelpCenter):
    try:
        assignments = list(help_center.badge_assignments.list_all())
    except NotFound:
        pytest.skip("Gather badge assignments not enabled on this account")
    assert isinstance(assignments, list)


def test_create_get_update_delete_badge(help_center: HelpCenter):
    try:
        categories = list(help_center.badge_categories.list_all())
    except NotFound:
        pytest.skip("Gather not enabled on this account")
    if not categories:
        pytest.skip("No badge categories found")

    badge = help_center.badges.create(
        badge_category_id=categories[0].id,
        name="Integration Test Badge",
        description="Test",
    )
    assert badge.id is not None

    try:
        fetched = help_center.badges.get(badge_id=badge.id)
        assert fetched.id == badge.id
    finally:
        help_center.badges.delete(badge_id=badge.id)
