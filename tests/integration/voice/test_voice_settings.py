from libzapi import Voice


def test_get_voice_settings(voice: Voice):
    settings = voice.voice_settings.get()
    assert settings is not None
