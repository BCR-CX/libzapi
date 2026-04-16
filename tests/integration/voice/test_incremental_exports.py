import time
from libzapi import Voice


def test_incremental_calls(voice: Voice):
    one_day_ago = int(time.time()) - 86400
    calls = list(voice.incremental_exports.calls(start_time=one_day_ago))
    assert isinstance(calls, list)


def test_incremental_legs(voice: Voice):
    one_day_ago = int(time.time()) - 86400
    legs = list(voice.incremental_exports.legs(start_time=one_day_ago))
    assert isinstance(legs, list)
