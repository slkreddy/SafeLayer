from safelayer.guards.pii import PIIGuard
from safelayer.guards.tone import ToneGuard
from safelayer.manager import GuardManager

def test_manager_cleans_text():
    guards = [PIIGuard(), ToneGuard()]
    manager = GuardManager(guards)
    input_str = "Email me at foo@bar.com. This is crap."
    output = manager.run(input_str)
    assert "[EMAIL MASKED]" in output
    assert "****" in output
