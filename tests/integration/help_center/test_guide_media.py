import pytest
import requests

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_guide_media(help_center: HelpCenter):
    try:
        media = list(help_center.guide_media.list_all())
    except NotFound:
        pytest.skip("Guide media not available on this account")
    assert isinstance(media, list)


def test_create_get_delete_guide_media(help_center: HelpCenter):
    # Minimal valid 1x1 PNG
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00"
        b"\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00"
        b"\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    try:
        media = help_center.guide_media.create(
            file=("test.png", png_bytes, "image/png"),
        )
    except (NotFound, requests.exceptions.HTTPError):
        pytest.skip("Guide media upload not available on this account")
    assert media.id is not None

    try:
        fetched = help_center.guide_media.get(media_id=media.id)
        assert fetched.id == media.id
    finally:
        help_center.guide_media.delete(media_id=media.id)
