import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_themes(help_center: HelpCenter):
    try:
        themes = list(help_center.themes.list_all())
    except NotFound:
        pytest.skip("Themes not available on this account")
    assert isinstance(themes, list)


def test_get_theme(help_center: HelpCenter):
    try:
        themes = list(help_center.themes.list_all())
    except NotFound:
        pytest.skip("Themes not available on this account")
    if not themes:
        pytest.skip("No themes found")
    theme = help_center.themes.get(theme_id=themes[0].id)
    assert theme.id == themes[0].id
