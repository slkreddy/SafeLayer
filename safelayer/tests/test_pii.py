from safelayer.guards.pii import PIIGuard

def test_email_masking():
    guard = PIIGuard()
    input_str = "Contact: jane.doe@example.com"
    masked = guard.mask(input_str)
    assert "[EMAIL MASKED]" in masked

def test_phone_masking():
    guard = PIIGuard()
    input_str = "Call me at 9876543210."
    masked = guard.mask(input_str)
    assert "[PHONE MASKED]" in masked

def test_check_email_and_phone():
    guard = PIIGuard()
    input_str = "john@foo.com 9876543210"
    findings = guard.check(input_str)
    assert any('email' in d['entity'] or 'EMAIL_ADDRESS' in d['entity'] for d in findings)
    assert any('phone' in d['entity'] or 'PHONE_NUMBER' in d['entity'] for d in findings)
