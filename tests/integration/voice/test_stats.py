from libzapi import Voice


def test_account_overview(voice: Voice):
    overview = voice.stats.account_overview()
    assert overview is not None
    assert overview.total_calls >= 0


def test_agents_activity(voice: Voice):
    agents = voice.stats.agents_activity()
    assert isinstance(agents, list)


def test_agents_overview(voice: Voice):
    overview = voice.stats.agents_overview()
    assert overview is not None


def test_current_queue_activity(voice: Voice):
    activity = voice.stats.current_queue_activity()
    assert activity is not None
    assert activity.agents_online >= 0
