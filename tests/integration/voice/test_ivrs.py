import pytest
from libzapi import Voice


def test_list_ivrs(voice: Voice):
    ivrs = list(voice.ivrs.list_all())
    assert isinstance(ivrs, list)


def test_list_and_get_ivr(voice: Voice):
    ivrs = list(voice.ivrs.list_all())
    if not ivrs:
        pytest.skip("No IVRs found")
    ivr = voice.ivrs.get(ivrs[0].id)
    assert ivr.id == ivrs[0].id


def test_list_ivr_menus(voice: Voice):
    ivrs = list(voice.ivrs.list_all())
    if not ivrs:
        pytest.skip("No IVRs found")
    menus = list(voice.ivr_menus.list_all(ivrs[0].id))
    assert isinstance(menus, list)


def test_list_ivr_routes(voice: Voice):
    ivrs = list(voice.ivrs.list_all())
    if not ivrs:
        pytest.skip("No IVRs found")
    menus = list(voice.ivr_menus.list_all(ivrs[0].id))
    if not menus:
        pytest.skip("No IVR menus found")
    routes = list(voice.ivr_routes.list_all(ivrs[0].id, menus[0].id))
    assert isinstance(routes, list)
