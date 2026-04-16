import pytest
from libzapi import Voice


def test_get_digital_line(voice: Voice):
    # Digital lines have no list endpoint, skip if ID unknown
    pytest.skip("Digital line ID required - no list endpoint available")
