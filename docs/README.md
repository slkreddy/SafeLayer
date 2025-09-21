# SafeLayer (SL) — Agentic Python Guardrails

**SafeLayer (SL)** is a modular, agentic Python library providing composable guardrails for LLM and agent-based AI systems. Use SafeLayer to enforce PII controls, tone filtering, TTS safety, or custom guard logic—at function boundaries, tool-call wrappers, agent frameworks, or service integration points.

---

## Features

- ✅ Composable Guards: PII, Tone, TTS and easy custom extension.
- ✅ Pluggable Decorators: Add as @decorator or via GuardManager in flows.
- ✅ No Dependencies: Pure Python; fast regex, optional Presidio for advanced PII.
- ✅ Audit-Friendly: Built-in logging & explainability (for compliance).
- ✅ Testable: All guards and logic can be unit tested and inspected.
- ✅ Enterprise Readiness: Professional code, no banners or intrusive logos.

---

## Quickstart


## Quickstart

```
from safelayer.guards import PIIGuard, ToneGuard
from safelayer.manager import GuardManager

guards = [PIIGuard(), ToneGuard(warn_only=True)]
manager = GuardManager(guards)

text = "Hi, my email is john.doe@gmail.com. Damn, that's crazy!"
cleaned = manager.run(text)
print(cleaned)
# Output: "Hi, my email is [EMAIL MASKED]. ****, that's crazy!"
```

### Function Decorator Pattern

```
from safelayer.decorators import apply_guards

@apply_guards(manager)
def agent_response():
    return "Contact me at alice@acme.com. Crap!"

print(agent_response())
# Output: "Contact me at [EMAIL MASKED]. ****!"
```

---

## Extending with Custom Guards

Create your own guard by inheriting `BaseGuard`:

```
from safelayer.guards.base import BaseGuard

class CustomGuard(BaseGuard):
    def check(self, text):
        # Your detection logic...
        return [{"entity": "custom", "start": 0, "end": 4, "explanation": "Example"}]

    def mask(self, text):
        return text.replace('bad', '[REDACTED]')
```

---

## Tests

Run all built-in unit tests (pytest-style):

```
python -m pytest tests/
```

---

## Documentation

- See `docs/architecture.md` for technical design.
- See `docs/developer_guide.md` for custom guard authoring.
- Example workflows in `examples/`.


## License

Apache 2.0 (c) 2025 [LaxmiKumar Sammeta](https://github.com/slkreddy/)

## Repository

https://github.com/slkreddy/SafeLayer/
```

