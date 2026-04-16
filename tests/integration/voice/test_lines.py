from libzapi import Voice


def test_list_lines(voice: Voice):
    lines = list(voice.lines.list_all())
    assert isinstance(lines, list)
