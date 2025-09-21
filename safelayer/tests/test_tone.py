from safelayer.guards.tone import ToneGuard

def test_profane_word_masking():
    guard = ToneGuard()
    input_str = "This is crap."
    masked = guard.mask(input_str)
    assert "****" in masked

def test_check_profane_word():
    guard = ToneGuard()
    input_str = "Damn, that's bad!"
    findings = guard.check(input_str)
    assert any('profanity' in d['entity'] for d in findings)
    assert any('Damn' in d['explanation'] for d in findings)
