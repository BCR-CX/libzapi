import uuid

import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_content_tags(help_center: HelpCenter):
    try:
        tags = list(help_center.content_tags.list_all())
    except NotFound:
        pytest.skip("Content tags not available on this account")
    assert isinstance(tags, list)


def test_create_get_update_delete_content_tag(help_center: HelpCenter):
    unique = str(uuid.uuid4())[:8]
    try:
        tag = help_center.content_tags.create(name=f"inttest-{unique}")
    except NotFound:
        pytest.skip("Content tags not available on this account")
    assert tag.id is not None

    try:
        fetched = help_center.content_tags.get(content_tag_id=tag.id)
        assert fetched.id == tag.id

        updated = help_center.content_tags.update(content_tag_id=tag.id, name=f"updated-{unique}")
        assert updated.name == f"updated-{unique}"
    finally:
        help_center.content_tags.delete(content_tag_id=tag.id)
