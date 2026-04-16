import pytest
from libzapi import Voice


def test_get_availability(voice: Voice):
    # Need a known agent ID - skip if unavailable
    pytest.skip("Agent ID required for availability test")
