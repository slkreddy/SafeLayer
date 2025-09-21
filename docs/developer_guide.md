
```markdown
# SafeLayer Developer Guide

This guide helps extend, test, and integrate SafeLayer guardrails in agentic workflows.

---

## Folder Structure

```
SafeLayer/
  safelayer/
    safelayer/
      manager.py
      decorators.py
      audit.py
      guards/
        base.py
        pii.py
        tone.py
        tts.py
    docs/
      README.md
      developer_guide.md
      architecture.md
    examples/
    tests/
```

---

## Creating a Custom Guard

To build a new guard:

1. **Inherit `BaseGuard`**
2. **Implement `check()` for detection**  
3. **Implement `mask()` for redaction/modification**

Example:

```
from safelayer.guards.base import BaseGuard

class CustomGuard(BaseGuard):
    def check(self, text):
        issues = []
        if 'secret' in text:
            issues.append({"entity": "secret", "start": text.index('secret'), "end": text.index('secret') + 6, "explanation": "Secret word detected"})
        return issues

    def mask(self, text):
        return text.replace('secret', '[REDACTED]')
```

---

## Plugging Into Guards

- **Via GuardManager:**
  ```
  guards = [MyGuard(), PIIGuard()]
  manager = GuardManager(guards)
  result = manager.run(text)
  ```

- **Function Decorator:**
  ```
  @apply_guards(manager)
  def agent_reply():
      return "..."
  ```

---

## Testing Guards

Create unit tests in `tests/` using pytest:

```
from safelayer.guards.pii import PIIGuard

def test_pii_masking():
    guard = PIIGuard()
    assert "[EMAIL MASKED]" in guard.mask("foo@bar.com")
```

Run tests:

```
python -m pytest tests/
```

---

## Contribution Guidelines

- Follow PEP-8 style
- Document new guards in `docs/`
- Provide CLI or API usage samples if extending



***

Reply “next” for the following file (architecture.md, examples, or tests), or request any specific type next.
